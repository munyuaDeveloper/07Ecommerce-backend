from users.models import CustomUser
from rest_framework import serializers

from product.models import Product
from category.models import Category

from shared_functions import service_responses

service_response = service_responses.ServiceResponseManager()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_product_images')
    seller = serializers.SerializerMethodField('get_product_seller')

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description',
            'price', 'quantity', 'images',
            "seller"
        ]

    def get_product_images(self, obj):
        image = list(obj.product_image.values_list('image', flat=True))
        images = ','.join(image)
        image_urls = service_response.get_image_urls(images)
        return image_urls

    def get_product_seller(self, obj):
        seller = obj.seller
        seller_details = UserSerializer(seller, many=False).data
        return seller_details


class ProductListSerializer(ProductSerializer):
    category = serializers.SerializerMethodField('get_product_category')

    class Meta:
        model = Product
        fields = ProductSerializer.Meta.fields + ['category']

    def get_product_category(self, obj):
        category = obj.category.all()
        category_details = CategorySerializer(category, many=True).data
        return category_details


class ProductCreateSerializer(serializers.Serializer):
    category = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    images = serializers.ListField(child=serializers.CharField())

    def validate_category(self, category):
        category_query = Category.objects.filter(name=category)
        if not category_query.exists():
            raise serializers.ValidationError("Add a valid category")
        return category
