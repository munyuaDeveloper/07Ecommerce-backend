from django.core.validators import RegexValidator
from rest_framework import serializers

from cart import models as cart_models

from product.serializers import ProductListSerializer


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


class ListWishListDetailSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField("get_product_details")

    class Meta:
        model = cart_models.WishList
        fields = ['id', 'product', 'date_created']

    def get_product_details(self, obj):
        product = obj.product
        product_details = ProductListSerializer(product, many=False).data
        return product_details


PAYMENT_OPTIONS = [
    ("PAYPAL", 'PAYPAL'),
    ("CARD", 'CARD'),
]


class OrderCreateSerializer(serializers.Serializer):
    cart = serializers.CharField()
    pickup_location = serializers.CharField()
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField()
    method_of_payment = serializers.ChoiceField(choices=PAYMENT_OPTIONS)
    card_owner = serializers.CharField(allow_blank=True, allow_null=True)
    card_number = serializers.CharField(allow_blank=True, allow_null=True)
    card_cvc = serializers.CharField(allow_blank=True, allow_null=True)

    def validate(self, attrs):
        method_of_payment = attrs['method_of_payment']
        card_owner = attrs['card_owner']
        card_number = attrs['card_number']
        card_cvc = attrs['card_cvc']

        if method_of_payment == 'CARD':
            if not bool(card_owner) or not bool(card_number):
                raise serializers.ValidationError(
                    "Please add card owner or number or cvc")

        return attrs


class OrderDetailSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField("get_cart_details")
    order_status = serializers.SerializerMethodField("get_order_status")

    class Meta:
        model = cart_models.OrderInfo
        fields = [
            'id',
            'order_reference',
            'payment_status',
            'order_status',
            'order_mount',
            'pickup_location',
            'phone_number',
            'email',
            'method_of_payment',
            'card_owner',
            'card_number',
            'card_cvc',
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

    def get_order_status(self, obj):
        cart = obj.cart
        if not cart:
            return []
        return cart.cart_status
