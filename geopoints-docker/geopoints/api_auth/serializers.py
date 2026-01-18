from rest_framework import serializers
from django.contrib.auth import authenticate
from .services import TokenJWT
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    password = serializers.CharField(
        required=True,
        max_length=150,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            raise serializers.ValidationError('Invalid username or password')
        attrs['user'] = user
        return attrs


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        required=True,
        max_length=300
    )

    def validate(self, attrs):
        token_service = TokenJWT()
        user = token_service.validate_refresh_token(attrs.get('refresh'))
        if user:
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Invalid token')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'password2']
