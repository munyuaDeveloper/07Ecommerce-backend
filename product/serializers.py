from rest_framework import serializers
import requests

from product.models import Product
from category.models import Category

from shared_functions import service_responses

service_response = service_responses.ServiceResponseManager()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_product_category')
    images = serializers.SerializerMethodField('get_product_images')

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'category',
                  'price', 'num_in_stock', 'images')

    def get_product_images(self, obj):
        image = list(obj.product_image.values_list('image', flat=True))
        images = ','.join(image)
        image_urls = service_response.get_image_urls(images)
        return image_urls

    def get_product_category(self, obj):
        category = obj.category.all()
        category_details = CategorySerializer(category, many=True).data
        return category_details


class ProductCreateSerializer(serializers.Serializer):
    category = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    images = serializers.ListField(child=serializers.CharField())

    def validate_category(self, category):
        category_query = Category.objects.filter(name=category)
        if not category_query.exists():
            raise serializers.ValidationError("Add a valid category")
        return category
