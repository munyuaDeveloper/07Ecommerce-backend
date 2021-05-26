from django.core.validators import RegexValidator
from rest_framework import serializers

from cart import models as cart_models

from product.serializers import ProductListSerializer


phone_regex = RegexValidator(
    regex=r'^\+?254?\d{10,12}$',
    message="Phone number must be entered in the format: '+254123456789'. Up to 12 digits allowed.")


class GenericRequestSerializer(serializers.Serializer):
    request_id = serializers.CharField()


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


class ListCartDetailSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField("get_cart_details")

    class Meta:
        model = cart_models.ShoppingCart
        fields = ['id', 'cart_status', 'cart']

    def get_cart_details(self, obj):
        cart_items = obj.cart_items.all()
        cart_details = CartDetailSerializer(cart_items, many=True).data
        return cart_details


class OrderCreateSerializer(serializers.Serializer):
    cart = serializers.CharField()
    pickup_location = serializers.CharField()
    phone_number = serializers.CharField(
        required=True, validators=[phone_regex])
    email = serializers.EmailField()


class OrderDetailSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField("get_cart_details")

    class Meta:
        model = cart_models.OrderInfo
        fields = [
            'id',
            'order_reference',
            'payment_status',
            'order_mount',
            'pickup_location',
            'phone_number',
            'email',
            'cart',
            'date_created',
        ]

    def get_cart_details(self, obj):
        cart = obj.cart
        if not cart:
            return []
        items = cart.cart_items.all()
        cart_details = CartDetailSerializer(items, many=True).data
        return cart_details
