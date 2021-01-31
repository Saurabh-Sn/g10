from rest_framework import serializers
from .models import Category, Product,  Brand


class categorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'code']


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['name', 'id']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'code',  'mfg_date', 'category', 'brand']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ListCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'code' ]


class ListProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'mfg_date', 'category', 'brand']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_category(self, obj):
        return obj.category.name

    def get_brand(self, obj):
        return obj.brand.name