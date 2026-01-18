from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models


class Point(models.Model):
    '''
    Географическая точчка на карте
    '''
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='points',
        verbose_name='Пользователь'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название точки'
    )
    description = models.TextField(
        verbose_name='Описание точки'
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Долгота"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    @property
    def coordinates(self):
        return float(self.latitude), float(self.longitude)

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"


class Message(models.Model):
    '''
    Сообщение к географической точке
    '''
    point = models.ForeignKey(
        'Point',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Точка'
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Пользователь'
    )
    content = models.TextField(
        verbose_name='Текст сообщения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    def __str__(self):
        return f"Сообщение от {self.user.username} к {self.point.name}"
