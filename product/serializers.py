from django.contrib.auth import models
from django.db.models import Max, Min
from rest_framework import serializers

from product.models import Product, ProductImage
from category.serializers import CategorySerializer
from category.models import Category

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = ProductImage
        fields = ['image']

    def get_image_url(self,obj):
        request = self.context.get('request')
        image = obj.image.url
        full_url = request.build_absolute_uri(image)
        return full_url

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name']
    

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_product_category')
    image = serializers.SerializerMethodField('get_product_image')

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'price', 'image')

    def get_product_image(self, obj):
        image = obj.product_image.all()

        image_details = ImageSerializer(image, many=True, context=self.context).data
        return image_details
    def get_product_category(self, obj):
        category = obj.category.all()
        category_details = CategorySerializer(category, many=True).data
        return category_details