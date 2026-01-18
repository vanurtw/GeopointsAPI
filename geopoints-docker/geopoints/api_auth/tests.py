from django.test import TestCase
import json
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .services import TokenJWT


class JWTAuthUnittestTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')

        self.user_data = {
            'username': 'usertest',
            'email': 'usertest@example.com',
            'password': 'usertest12345',
            'password2': 'usertest12345'
        }

        self.login_data = {
            'username': 'usertest',
            'password': 'usertest12345'
        }

    def test_register_user_success(self):
        """Регистрация пользователя"""

        response = self.client.post(
            self.register_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
        self.assertIn('user', response.json())

        user_exists = self.user_model.objects.filter(username='usertest').exists()
        self.assertTrue(user_exists)

        user = self.user_model.objects.get(username='usertest')
        self.assertEqual(user.email, 'usertest@example.com')
        self.assertTrue(user.check_password('usertest12345'))

    def test_login_user_success(self):
        """Вход пользователя успешный"""

        user = self.user_model.objects.create_user(
            username='usertest',
            email='usertest@example.com',
            password='usertest12345',
        )
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.login_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

        access = response.json()['access']
        refresh = response.json()['refresh']

        self.assertTrue(len(access) > 10)
        self.assertTrue(len(refresh) > 10)

        access_token = TokenJWT().create_token(user=user, token_typ='access')
        refresh_token = TokenJWT().create_token(user=user, token_typ='refresh')

        self.assertEqual(access, access_token)
        self.assertEqual(refresh, refresh_token)

    def test_login_with_invalid_credentials(self):
        """Вход с неправильными данными"""

        self.user_model.objects.create_user(
            username='usertest',
            email="usertest@example.com",
            password="usertest12345"
        )

        invalid_data = {
            "username": "usertest",
            "password": "wrong_password_usertest12345"
        }

        response = self.client.post(
            self.login_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())

    def test_registration_invalid_password(self):
        """Ощибка регистрации с несовпадающими праолями"""

        invalid_data = self.user_data
        invalid_data['password2'] += '_invalid_password'

        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())

        user_exists = self.user_model.objects.filter(username=self.user_data['username']).exists()
        self.assertFalse(user_exists)

    def test_registration_duplicate_username(self):
        """Ошибка регистрации пользователя с уже существующим username в БД"""

        self.user_model.objects.create_user(
            username='user',
            email='user1@example.com',
            password='password12345'
        )

        response = self.client.post(
            self.register_url,
            data={
                'username': 'user',
                'email': 'user2@example.com',
                'password': 'password12345password',
                'password2': 'password12345password'
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json())

    def test_empty_strings_in_data(self):
        """Пустые строки в данных должны обрабатываться"""

        response = self.client.post(
            self.register_url,
            data={
                'username': '',
                'email': '',
                'password': 'usertest12345',
                'password2': 'usertest12345'
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_http_method(self):
        """get запрос к post endpoint"""

        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
