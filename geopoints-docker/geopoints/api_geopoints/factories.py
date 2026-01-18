import factory
from django.contrib.auth import get_user_model
from .models import Point, Message
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    password = factory.PostGenerationMethodCall('set_password', f'{username}12345')


class PointFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Point

    user = factory.SubFactory(UserFactory)
    name = factory.LazyFunction(lambda: fake.name())
    description = factory.LazyFunction(lambda: fake.text())
    latitude = factory.LazyFunction(lambda: fake.latitude())
    longitude = factory.LazyFunction(lambda: fake.longitude())


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    point = factory.SubFactory(PointFactory)
    user = factory.SubFactory(UserFactory)
    content = factory.LazyFunction(lambda: fake.text())
