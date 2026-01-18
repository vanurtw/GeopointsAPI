from django.contrib import admin
from django.urls import path, include
from .swagger_urls import urlpatterns as swga_url
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('api_auth.urls')),
    path('api/', include('api_geopoints.urls')),

]

if settings.DEBUG:
    urlpatterns += swga_url
    urlpatterns += debug_toolbar_urls()
