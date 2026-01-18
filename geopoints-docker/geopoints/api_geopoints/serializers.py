from rest_framework import serializers
from .models import Point, Message
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']


class PointSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Point
        fields = [
            'id',
            'user',
            'name',
            'description',
            'latitude',
            'longitude',
            'created_at',
            'update_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'update_at']

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Диапозон широты от -90 до 90")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Диапозон долготы от -180 до 180")
        return value


class SearchSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(
        decimal_places=6,
        max_digits=10,
        required=True,
        help_text='Широта центральной точки'
    )
    longitude = serializers.DecimalField(
        decimal_places=6,
        max_digits=10,
        required=True,
        help_text='Долгота центральной точки'
    )

    radius = serializers.DecimalField(
        decimal_places=2,
        max_digits=10,
        max_value=1000,
        min_value=0.1,
        help_text='Радиус поиска в км (0.1-1000)'
    )

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Диапозон широты от -90 до 90")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Диапозон долготы от -180 до 180")
        return value


class MessageSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('detail', True):
            point_id = data.pop('point')
            query = self.context.get('query', Message.objects.filter(point__id=point_id))
            for mes in query:
                if  mes.point.id == point_id:
                    point_serializer = PointSerializer(mes.point)
                    data['point'] = point_serializer.data
        return data

    class Meta:
        model = Message
        fields = [
            'id',
            'point',
            'content',
            'created_at'
        ]

        read_only_fields = ['id', 'user', ]
