from .services import TokenJWT


class CreateTokenMixins:
    '''Миксин для создания пары токенов access, refresh'''

    def create_token_pair(self, user):
        '''Возвращает пару токенов'''

        token_service = TokenJWT()
        access = token_service.create_token(user, 'access')
        refresh = token_service.create_token(user, 'refresh')
        return access, refresh
