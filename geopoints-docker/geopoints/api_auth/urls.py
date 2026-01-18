from django.urls import path
from .views import TokenObtainPairView, TokenRefreshView, RegisterView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegisterView.as_view(), name='register'),
]
