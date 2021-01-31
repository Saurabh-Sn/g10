from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Category, Brand
from .serializers import (categorySerializer, ListCategorySerializer, BrandSerializer, ListProductSerializer,
                          ProductSerializer)

from common.pagination import DefaultPagination


class CategoryView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = categorySerializer
    queryset = Category.objects.filter(is_deleted=False)
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        serializer = categorySerializer
        if self.action == 'list' or self.action == 'retrieve':
            serializer = ListCategorySerializer
        return serializer

    @action(methods=['DELETE'], detail=False, url_path='category/(?P<pk>\d+)', url_name='delete')
    def delete_category(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        category.is_deleted = True
        category.update()
        for products in category.product_category.all():
            products.is_deleted = True
            products.update()
        return Response({'messages': 'deleted successful.'}, status=status.HTTP_204_NO_CONTENT)


class BrandView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    serializer_class = BrandSerializer
    pagination_class = DefaultPagination
    queryset = Brand.objects.filter(is_deleted=False)

    @action(methods=['DELETE'], detail=False, url_path='brands/(?P<pk>\d+)', url_name='delete')
    def delete_brand(self, request, pk=None):
        brand = get_object_or_404(Brand, id=pk)
        brand.is_deleted = True
        brand.update()
        for products in brand.product_brand.all():
            products.is_deleted = True
            products.update()
        return Response({'messages': 'deleted successful.'}, status=status.HTTP_204_NO_CONTENT)


class ProductView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    queryset = Product.objects.filter(is_deleted=False)

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        if 'mf_year' in self.request.query_params:
            queryset = queryset.filter(mfg_date__year=mf_year)
        return queryset

    def get_serializer_class(self):
        serializer = ProductSerializer
        if self.action == 'list' or self.action == 'retrieve':
            serializer = ListProductSerializer
        return serializer

    @action(methods=['DELETE'], detail=False, url_path='product/(?P<pk>\d+)', url_name='delete')
    def delete_product(self, request, pk=None):
        product = get_object_or_404(Product, id=pk)
        product.is_deleted = True
        product.update()
        return Response({'messages': 'deleted successful.'}, status=status.HTTP_204_NO_CONTENT)