from django.test import TestCase
from .factories import UserFactory, PointFactory, MessageFactory
from .serializers import PointSerializer, MessageSerializer
from django.urls import reverse
from rest_framework import status
from api_auth.services import TokenJWT
import json
from .models import Point, Message
from rest_framework.test import APIClient
import math


class ModelUnittestTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.point = PointFactory(user=self.user)
        self.message = MessageFactory(point=self.point, user=self.user)

    def test_create_point(self):
        """Тест создания точки на карте"""

        self.assertEqual(self.point.name, self.point.name)
        self.assertEqual(self.point.user, self.user)

    def test_create_message(self):
        """Тест создания сообщения к точке"""

        self.assertEqual(self.message.point, self.point)
        self.assertEqual(self.message.user, self.user)

    def test_message_post_relationship(self):
        """Тест проверки созания связи между несколькими сообщениями к одной точке"""
        MessageFactory(user=self.user, point=self.point)
        MessageFactory(user=self.user, point=self.point)
        self.assertEqual(self.point.messages.count(), 3)


class PointSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.point = PointFactory(
            name='Test Point',
            user=self.user,
            description='Test Description',
            latitude=55.7558,
            longitude=37.6173,
        )
        self.point_data = {
            'name': 'Test Point',
            'description': 'Test Description',
            'latitude': 55.7558,
            'longitude': 37.6173,
        }


def test_valid_serializer(self):
    """Тест валидного сериализатора"""
    serializer = PointSerializer(data=self.point_data)
    self.assertTrue(serializer.is_valid())


def test_create_point(self):
    """Тест создания точки через сериализатор"""
    serializer = PointSerializer(data=self.point_data, )
    self.assertTrue(serializer.is_valid())

    point = serializer.save(user=self.user)

    self.assertEqual(point.name, 'Test Point')
    self.assertEqual(point.user, self.user)
    self.assertEqual(float(point.longitude), self.point_data['longitude'])
    self.assertEqual(float(point.latitude), self.point_data['latitude'])


def test_serializer_output(self):
    """Тест вывода сериализатора"""
    point = PointFactory(user=self.user)

    serializer = PointSerializer(point)

    data = serializer.data
    self.assertEqual(data['name'], point.name)
    self.assertEqual(data['description'], point.description)
    self.assertIn('user', data)
    self.assertIn('latitude', data)
    self.assertIn('longitude', data)
    self.assertIn('created_at', data)
    self.assertIn('update_at', data)


def test_invalid_coordinates(self):
    """Тест невалидных координат"""

    invalid_data = self.point_data.copy()
    invalid_data['latitude'] = 100.0

    serializer = PointSerializer(data=invalid_data, )
    self.assertFalse(serializer.is_valid())


class MessageSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.point = PointFactory()
        self.message = MessageFactory(point=self.point, user=self.user)
        self.message_data = {
            'content': 'Test message content',
            'point': self.point.id
        }

    def test_create_message(self):
        """Тест создания сообщения"""

        serializer = MessageSerializer(data=self.message_data)
        self.assertTrue(serializer.is_valid())
        message = serializer.save(user=self.user)

        self.assertEqual(message.content, 'Test message content')
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.point, self.point)

    def test_serializer_output(self):
        """Тест вывода сериализатора"""

        serializer = MessageSerializer(self.message)

        data = serializer.data
        self.assertIn('id', data)
        self.assertIn('point', data)
        self.assertIn('user', data)
        self.assertIn('content', data)
        self.assertIn('created_at', data)


class PointViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.point = PointFactory(user=self.user)
        self.access_token = TokenJWT().create_token(user=self.user, token_typ='access')
        self.point_url = reverse('points')
        self.search_point_url = reverse('points-search_in_radius')


def test_list_points_unauthenticated(self):
    """Тест получения списка точек без аутентификации"""

    response_points = self.client.get(self.point_url)
    response_search_points = self.client.get(self.search_point_url)
    self.assertEqual(response_points.status_code, status.HTTP_403_FORBIDDEN)
    self.assertEqual(response_search_points.status_code, status.HTTP_403_FORBIDDEN)


def test_create_point_authenticated(self):
    """Тест создания точки с аутентификацией"""

    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    data = {
        'name': 'New Point',
        'description': 'New Description',
        'latitude': 55.7558,
        'longitude': 37.6173,
    }
    response = self.client.post(
        self.point_url,
        data=json.dumps(data),
        content_type='application/json'
    )

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Point.objects.count(), 2)
    self.assertEqual(response.data['name'], 'New Point')
    self.assertEqual(response.data['user']['username'], self.user.username)


def test_create_point_unauthenticated(self):
    """Тест создания точки без аутентификации"""

    data = {
        'title': 'New Point',
        'latitude': 55.7558,
        'longitude': 37.6173,
    }

    response = self.client.post(
        self.point_url,
        data=json.dumps(data),
        content_type='application/json'
    )
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


def test_search_point_in_radius(self):
    """Поиск точек по параметрам"""

    latitude = 34.20
    longitude = 40.12
    delta_lat = lambda x, del_x_km=0: x + (del_x_km / 111)
    delta_lon = lambda x, del_x_km=0: x + (del_x_km / (111 * math.cos(math.radians(x))))

    Point.objects.all().delete()

    PointFactory(user=self.user, latitude=latitude, longitude=longitude)  # 1

    PointFactory(user=self.user, latitude=delta_lat(latitude, 9), longitude=delta_lon(longitude, 3))  # 2
    PointFactory(user=self.user, latitude=delta_lat(latitude, 10), longitude=delta_lon(longitude, 5))  # 3

    PointFactory(user=self.user, latitude=delta_lat(latitude, 55), longitude=delta_lon(longitude, 60))
    PointFactory(user=self.user, latitude=delta_lat(latitude, 20), longitude=delta_lon(longitude, 19))
    PointFactory(user=self.user, latitude=delta_lat(latitude, 30), longitude=delta_lon(longitude, 60))
    PointFactory(user=self.user, latitude=delta_lat(latitude, 45), longitude=delta_lon(longitude, 22))

    radius = 15

    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    response = self.client.get(
        self.search_point_url,
        data={"latitude": latitude, "longitude": longitude, "radius": radius},
        content_type='application/json'
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.json()), 3)


class MessageViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.point = PointFactory(user=self.user)
        self.message = MessageFactory(user=self.user, point=self.point)
        self.access_token = TokenJWT().create_token(user=self.user, token_typ='access')
        self.messages_url = reverse('messages')
        self.search_message_url = reverse('messages-search_in_radius')

    def test_list_messages(self):
        """Тест получения списка сообщений пользователя"""

        MessageFactory(user=self.user, point=self.point)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.messages_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_list_messages_unauthenticated(self):
        """Тест получения списка сообщений без аутентификации"""

        response_messages = self.client.get(self.messages_url)
        response_search_message = self.client.get(self.search_message_url)
        self.assertEqual(response_messages.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_search_message.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_message_authenticated(self):
        """Тест создания сообщения с аутентификацией"""

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'point': self.point.id,
            'user': self.user.id,
            'content': 'Test content',
        }
        response = self.client.post(
            self.messages_url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(response.json()['user']['id'], self.user.id)
        self.assertEqual(response.json()['point']['id'], self.point.id)

    def test_create_message_unauthenticated(self):
        """Тест создания сообщения без аутентификации"""

        data = {
            'point': self.point.id,
            'user': self.user.id,
            'content': 'Test content',
        }

        response = self.client.post(
            self.messages_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_message_in_radius(self):
        """Поиск сообщений по параметрам"""

        latitude = 34.20
        longitude = 40.12
        delta_lat = lambda x, del_x_km=0: x + (del_x_km / 111)
        delta_lon = lambda x, del_x_km=0: x + (del_x_km / (111 * math.cos(math.radians(x))))

        Point.objects.all().delete()
        Message.objects.all().delete()

        p1 = PointFactory(user=self.user, latitude=latitude, longitude=longitude)  # 1

        p2 = PointFactory(user=self.user, latitude=delta_lat(latitude, 9), longitude=delta_lon(longitude, 3))  # 2
        p3 = PointFactory(user=self.user, latitude=delta_lat(latitude, 10), longitude=delta_lon(longitude, 5))  # 3

        p4 = PointFactory(user=self.user, latitude=delta_lat(latitude, 55), longitude=delta_lon(longitude, 60))
        p5 = PointFactory(user=self.user, latitude=delta_lat(latitude, 20), longitude=delta_lon(longitude, 19))
        p6 = PointFactory(user=self.user, latitude=delta_lat(latitude, 30), longitude=delta_lon(longitude, 60))
        p7 = PointFactory(user=self.user, latitude=delta_lat(latitude, 45), longitude=delta_lon(longitude, 22))

        MessageFactory(user=self.user, point=p1)  # 1
        MessageFactory(user=self.user, point=p2)  # 2
        MessageFactory(user=self.user, point=p3)  # 3

        MessageFactory(user=self.user, point=p4)
        MessageFactory(user=self.user, point=p5)
        MessageFactory(user=self.user, point=p6)
        MessageFactory(user=self.user, point=p7)
        MessageFactory(user=self.user, point=p7)

        radius = 15

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.get(
            self.search_message_url,
            data={"latitude": latitude, "longitude": longitude, "radius": radius},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
