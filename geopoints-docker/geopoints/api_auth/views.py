from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import LoginSerializer, RefreshSerializer, UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from api_geopoints.serializers import UserSerializer
from rest_framework import status
from .mixins import CreateTokenMixins
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TokenObtainPairView(GenericAPIView, CreateTokenMixins):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="Вход пользователя",
        operation_description="""
            Аутентификация пользователя по имени и паролю.
            - access - JWT токен для доступа к API 
            - refresh - JWT токен для обновления access токена
        """,
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Успешный вход",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='access JWT токен'
                        ),
                        'refresh': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='refresh JWT токен'
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка валидации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'non_field_errors': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            500: openapi.Response(
                description="Внутренняя ошибка сервера",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING
                        )
                    }
                )
            )
        },
        tags=['Пользователь']
    )
    def post(self, request):
        '''Вход пользователя'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            access, refresh = self.create_token_pair(user=user)
            return Response({
                'access': access,
                'refresh': refresh
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(GenericAPIView, CreateTokenMixins):
    serializer_class = RefreshSerializer

    @swagger_auto_schema(
        operation_summary="Обновление токенов",
        operation_description="""
            Обновление токенов
            - access - JWT токен для доступа к API 
            - refresh - JWT токен для обновления access токена
        """,
        request_body=RefreshSerializer,
        responses={
            200: openapi.Response(
                description="Токены обновлены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='access JWT токен'
                        ),
                        'refresh': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='refresh JWT токен'
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Неверный или просроченный refresh токен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'non_field_errors': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )
        },
        tags=['Пользователь']
    )
    def post(self, request):
        '''Возвращает новую пару токенов'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            access, refresh = self.create_token_pair(user=user)
            return Response({
                'access': access,
                'refresh': refresh
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(GenericAPIView, CreateTokenMixins):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="""
            После успешной регистрации сразу возвращаются JWT токены для входа.
        """,
        request_body=UserRegistrationSerializer,
        responses={
            200: openapi.Response(
                description="Токены обновлены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='access JWT токен'
                        ),
                        'refresh': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='refresh JWT токен'
                        ),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description='Данные созданного пользователя',
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка валидации данных",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'fields': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        ),
                        'non_field_errors': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )
        },
        tags=['Пользователь']
    )
    def post(self, request):
        '''Регистрация пользователя'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            access, refresh = self.create_token_pair(user=user)
            user_serializer = UserSerializer(user)
            return Response({
                'access': access,
                'refresh': refresh,
                'user': user_serializer.data
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
