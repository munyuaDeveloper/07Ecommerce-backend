import email
from users.models import CustomUser
import category
from rest_framework import serializers

from product.models import Product, ProductImage
from category.models import Category


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = ProductImage
        fields = ['image']

    def get_image_url(self, obj):
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

        image_details = ImageSerializer(
            image, many=True, context=self.context).data
        return image_details

    def get_product_category(self, obj):
        category = obj.category.all()
        category_details = CategorySerializer(category, many=True).data
        return category_details


class ProductImageSerializer(serializers.Serializer):
    image = serializers.CharField()
    is_main_image = serializers.BooleanField(default=False)


class ProductCreateSerializer(serializers.Serializer):
    category = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    images = ProductImageSerializer(many=True)

    def validate_category(self, category):
        category_query = Category.objects.filter(name=category)
        if not category_query.exists():
            raise serializers.ValidationError("Add a valid category")
        return category

    def validate(self, attrs):
        category = attrs.get('category')
        category_query = Category.objects.filter(name=category)
        if not category_query.exists():
            raise serializers.ValidationError("Add a valid category")
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        seller_email = request.user
        title = validated_data.get('title')
        desc = validated_data.get('description')
        price = validated_data.get('price')
        seller = CustomUser.objects.get(email=seller_email)

        product_params = {
            "title": title,
            "desc": desc,
            "price": price,
            "seller": seller
        }
        product_inst = Product.objects.get_or_create(**product_params)
