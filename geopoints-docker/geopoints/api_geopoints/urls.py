from django.urls import path
from .views import PointView, PointSearchView, MessageView, MessageSearchView

urlpatterns = [
    path('points/', PointView.as_view(), name='points'),
    path('points/search/', PointSearchView.as_view(), name='points-search_in_radius'),
    path('points/messages/', MessageView.as_view(), name='messages'),
    path('points/messages/search/', MessageSearchView.as_view(), name='messages-search_in_radius'),

]
