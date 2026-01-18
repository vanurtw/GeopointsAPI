import hmac
import time
from geopoints.settings import SECRET_KEY, JWT
import hashlib
import base64
import json
from django.contrib.auth import get_user_model


class TokenJWT:

    def build_token_payload(self, user, token_type: str) -> dict:
        payload = {i: getattr(user, i) for i in JWT['payload']}
        payload['iss'] = 'my-auth-server'
        payload['sub'] = user.id
        payload['iat'] = int(time.time())
        if token_type == 'access':
            lifetime = JWT['ACCESS_TOKEN_LIFETIME']
        else:
            lifetime = JWT['REFRESH_TOKEN_LIFETIME']
        payload['exp'] = int(time.time() + lifetime.total_seconds())
        payload['token_type'] = token_type
        return payload

    def create_token(self, user, token_typ) -> str:
        payload = self.build_token_payload(user, token_typ)
        header = JWT['header']
        payload_bs64 = self.encoding_bs64(payload)
        header_bs64 = self.encoding_bs64(header)
        signature = self.create_signature(header_bs64, payload_bs64)
        token = f'{header_bs64.decode()}.{payload_bs64.decode()}.{signature}'
        return token

    def validate_refresh_token(self, token):
        try:
            header_bs64, payload_bs64, signature = token.split('.')
        except ValueError:
            return False
        valid_sign = self.validate_signature(header_bs64, payload_bs64, signature)
        payload = self.decode_bs64(payload_bs64)
        token_valid = self.validate_token(payload, 'refresh')
        if valid_sign and token_valid:
            user = self.get_user(payload)
            return user
        return None

    @staticmethod
    def encoding_bs64(data: dict):
        data_str = json.dumps(data).encode()

        data_bs64 = base64.b64encode(data_str).replace(b'+', b'-').replace(b'/', b'_').rstrip(b'=')
        return data_bs64

    @staticmethod
    def create_signature(header_bs64, payload_bs64) -> str:
        msg = header_bs64 + b'.' + payload_bs64
        signature = hmac.new(key=SECRET_KEY.encode(), msg=msg, digestmod=hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature)
        signature_b64url = signature_b64.replace(b'+', b'-').replace(b'/', b'_').rstrip(b'=')

        return signature_b64url.decode('utf-8')

    @staticmethod
    def validate_signature(head_bs64, payload_bs64, signature) -> bool:
        valid_sign = TokenJWT.create_signature(head_bs64.encode(), payload_bs64.encode())
        return signature == valid_sign

    @staticmethod
    def decode_bs64(data: str) -> dict:
        padding = 4 - len(data) % 4
        if padding != 4:
            data += '=' * padding
        try:
            payload_str = base64.b64decode(data).decode()
        except Exception as e:
            raise ValueError(f"Invalid base64: {e}")
        payload = json.loads(payload_str)
        return payload

    @staticmethod
    def validate_token(payload: dict, token_type: str) -> bool:
        time_now = time.time()
        return time_now < payload['exp'] and payload['token_type'] == token_type

    @staticmethod
    def get_user(payload: dict):
        try:
            user = get_user_model().objects.get(id=payload['sub'])
            return user
        except get_user_model().DoesNotExist:
            return None
