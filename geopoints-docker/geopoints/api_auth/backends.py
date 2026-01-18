from rest_framework import authentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .services import TokenJWT
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class AuthenticationJWT(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = settings.JWT['AUTH_HEADER']
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return None, None
        parts = token.split()
        if len(parts) != 2 or parts[0] != auth_header:
            raise AuthenticationFailed(
                'Invalid Authorization header format. Expected: Bearer <token>',
                code='invalid_header'
            )
        head_token, token = parts
        try:
            header_bs64, payload_bs64, signature = token.split('.')
        except ValueError:
            raise AuthenticationFailed('Incorrect token form', code='invalid_token')
        if not TokenJWT.validate_signature(header_bs64, payload_bs64, signature):
            raise AuthenticationFailed('Signature verification failed', code='invalid_token')
        try:
            decode_payload = TokenJWT.decode_bs64(payload_bs64)
        except:
            raise AuthenticationFailed('Cannot decode token', code='decode_error')
        if not TokenJWT.validate_token(decode_payload, 'access'):
            raise AuthenticationFailed('Invalid token', code='invalid_token')
        user = get_object_or_404(get_user_model(), id=decode_payload['id'])
        return user, token
