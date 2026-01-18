from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PointSerializer, SearchSerializer, MessageSerializer
from .models import Point, Message
from .services import Location
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PointView(GenericAPIView):
    serializer_class = PointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Point.objects.filter(user=self.request.user).select_related('user')

    @swagger_auto_schema(
        operation_summary="Получение точек пользователя",
        operation_description="""
            Получение точек текущего пользователя
            Доступно только для авторизованных
        """,
        responses={
            401: openapi.Response(
                description="Ошибка авторизации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            403: openapi.Response(
                description="Доступ запрещен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )

        },
        tags=['Точки']
    )
    def get(self, request):
        """Возвращает точки текущего пользователя"""
        query = self.get_queryset()
        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Создание точки",
        operation_description="""
            Создание точки пользователя
            Доступно только для авторизованных
        """,
        responses={
            401: openapi.Response(
                description="Ошибка авторизации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            403: openapi.Response(
                description="Доступ запрещен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )

        },
        tags=['Точки']
    )
    def post(self, request):
        """Создание точки"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PointSearchView(GenericAPIView):
    serializer_class = PointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Point.objects.all().select_related('user')

    @swagger_auto_schema(
        operation_summary="Поиск точек в радиусе",
        operation_description="""
           Поиск географических точек в заданном радиусе от указанных координат.
        
        - latitude - широта центра поиска (обязательный)
        - longitude - долгота центра поиска (обязательный)  
        - radius - радиус поиска в метрах (обязательный)
        """,
        manual_parameters=[
            openapi.Parameter(
                'latitude',
                openapi.IN_QUERY,
                description="Широта центра поиска (от -90 до 90)",
                type=openapi.TYPE_NUMBER,
                format='float',
                required=True,
            ),
            openapi.Parameter(
                'longitude',
                openapi.IN_QUERY,
                description="Долгота центра поиска (от -180 до 180)",
                type=openapi.TYPE_NUMBER,
                format='float',
                required=True,
            ),
            openapi.Parameter(
                'radius',
                openapi.IN_QUERY,
                description="Радиус поиска в км",
                type=openapi.TYPE_NUMBER,
                format='float',
                required=True,
            ),
        ],
        responses={
            401: openapi.Response(
                description="Ошибка авторизации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            403: openapi.Response(
                description="Доступ запрещен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )

        },
        tags=['Точки']
    )
    def get(self, request):
        '''Возвращает точки по критериям отбора'''
        serializer = SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        center_lat, center_lon, radius = serializer.validated_data.values()
        loc = Location(center_lat, center_lon, radius)
        points = loc.get_points()
        data = [self.get_serializer(obj[1]).data for obj in points]
        return Response(data)


class MessageView(GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).select_related('point', 'point__user')

    @swagger_auto_schema(
        operation_summary="Создание сообщения к точке",
        operation_description="""
            Создание сообщения к точки пользователя
            Доступно только для авторизованных
        """,
        responses={
            401: openapi.Response(
                description="Ошибка авторизации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            403: openapi.Response(
                description="Доступ запрещен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )

        },
        tags=['Сообщения']
    )
    def post(self, request):
        """Создания сообщения к точке"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Получение сообщений пользователя",
        operation_description="""
            Получение сообщений текущего пользователя
            Доступно только для авторизованных
        """,
        responses={
            401: openapi.Response(
                description="Ошибка авторизации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            403: openapi.Response(
                description="Доступ запрещен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )

        },
        tags=['Сообщения']
    )
    def get(self, request):
        """Возвращает сообщения текущего пользователя"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'query': queryset})
        return Response(serializer.data)


class MessageSearchView(GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()

    @swagger_auto_schema(
        operation_summary="Поиск сообщений в радиусе",
        operation_description="""
               Поиск сообщений точек в заданном радиусе от указанных координат.

            - latitude - широта центра поиска (обязательный)
            - longitude - долгота центра поиска (обязательный)  
            - radius - радиус поиска в метрах (обязательный)
            """,
        manual_parameters=[
            openapi.Parameter(
                'latitude',
                openapi.IN_QUERY,
                description="Широта центра поиска (от -90 до 90)",
                type=openapi.TYPE_NUMBER,
                format='float',
                required=True,
            ),
            openapi.Parameter(
                'longitude',
                openapi.IN_QUERY,
                description="Долгота центра поиска (от -180 до 180)",
                type=openapi.TYPE_NUMBER,
                format='float',
                required=True,
            ),
            openapi.Parameter(
                'radius',
                openapi.IN_QUERY,
                description="Радиус поиска в км",
                type=openapi.TYPE_NUMBER,
                format='float',
                required=True,
            ),
        ],
        responses={
            401: openapi.Response(
                description="Ошибка авторизации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            403: openapi.Response(
                description="Доступ запрещен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )

        },
        tags=['Сообщения']
    )
    def get(self, request):
        '''Возвращает сообщения найденные по критериям отбора'''
        serializer = SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        center_lat, center_lon, radius = serializer.validated_data.values()
        loc = Location(center_lat, center_lon, radius)
        points = loc.get_points()
        point_ids = [point.id for _, point in points]
        messages = Message.objects.filter(
            point_id__in=point_ids
        ).select_related('point', 'point__user')
        message_serializer = MessageSerializer(messages, many=True, context={'query': messages})
        return Response(message_serializer.data)
