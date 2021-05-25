from rest_framework import serializers

from cart import models as cart_models

from product.serializers import ProductListSerializer


class AddToCartSerializer(serializers.Serializer):
    product = serializers.CharField()


class CartDetailSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField("get_product_details")

    class Meta:
        model = cart_models.ShoppingCartItem
        fields = ['id', 'products_num', 'product', 'total']

    def get_product_details(self, obj):
        product = obj.product
        product_details = ProductListSerializer(product, many=False).data
        return product_details


class OrderItemSerializer(serializers.Serializer):
    product = serializers.CharField()
    quantity = serializers.IntegerField()
    amount = serializers.IntegerField()


class OrderCreateSerializer(serializers.Serializer):
    pickup_location = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.CharField()
    items = OrderItemSerializer(many=True)
