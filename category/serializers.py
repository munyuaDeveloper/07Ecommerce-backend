from product.serializers import ProductSerializer
from category.models import Category
from rest_framework import serializers


class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        name = validated_data.get('name')
        name = name.upper()
        category = Category.objects.filter(name__icontains=name)
        if category.exists():
            category = category.first()
            response = {
                "name": category.name
            }
            return response

        Category.objects.create(name=name)
        response = {
            "name": name
        }
        return response


class ListCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class ListCategoryProductSerializer(ListCategorySerializer):
    products = serializers.SerializerMethodField("get_category_products")

    class Meta:
        model = Category
        fields = ListCategorySerializer.Meta.fields + [
            "products"
        ]

    def get_category_products(self, obj):
        products = obj.categories.all()
        product_details = ProductSerializer(products, many=True).data
        return product_details
