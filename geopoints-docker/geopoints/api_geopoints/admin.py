from django.contrib import admin
from .models import Point, Message


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', '__str__']
    list_display_links = ['id', 'name']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']
    list_display_links = ['id', '__str__']
    list_filter = ['user', 'point', 'created_at']
