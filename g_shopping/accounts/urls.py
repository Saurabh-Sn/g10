from django.urls import path, re_path, include
from rest_framework import routers
from .api import RegistrationView,  LoginView
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register('register', RegistrationView, 'register')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path(r'api/v1/login/token/', LoginView.as_view(), name='token_obtain'),
    path(r'api/v1/login/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]