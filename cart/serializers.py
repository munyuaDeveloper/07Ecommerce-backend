from rest_framework import serializers

from cart import models as cart_models

from product.serializers import ProductListSerializer


class AddToCartSerializer(serializers.Serializer):
    product = serializers.CharField()


class CartDetailSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField("get_product_details")

    class Meta:
        model = cart_models.ShoppingCartItem
        fields = ['products_num', 'product', 'total']

    def get_product_details(self, obj):
        product = obj.product
        product_details = ProductListSerializer(product, many=False).data
        return product_details
