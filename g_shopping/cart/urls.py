from django.urls import path, re_path, include
from rest_framework import routers
from .api import CartView

router = routers.DefaultRouter()
router.register('cart', CartView, 'cart')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]