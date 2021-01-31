from django.urls import path, re_path, include
from rest_framework import routers
from .api import CategoryView, BrandView, ProductView

router = routers.DefaultRouter()
router.register('categories', CategoryView, 'category')
router.register('brands', BrandView, 'brand')
router.register('product', ProductView, 'product')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]