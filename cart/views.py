from django.contrib.sessions.models import Session
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F

from cart import models as cart_models
from cart.serializers import AddToCartSerializer, CartDetailSerializer

from product.models import Product


class AddToCart(generics.CreateAPIView):
    queryset = cart_models.ShoppingCart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = (AllowAny, )

    def create(self, request):
        try:
            user = request.user
            session_id = request.session._get_or_create_session_key()
            if user.is_anonymous:
                user = None
        except Exception as e:
            print(e)
            pass

        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        product_id = payload['product']

        cart_params = {}
        if bool(user):
            cart_params.update({
                "user": user
            })
        else:
            cart_params.update({
                "session_id": session_id
            })

        cart, created = cart_models.ShoppingCart.objects.get_or_create(
            **cart_params)
        product = Product.objects.filter(id=product_id).first()
        update_product = cart_models.ShoppingCartItem.objects.filter(
            cart=cart, product=product).update(products_num=F('products_num') + 1)

        if update_product <= 0:
            product_param = {
                "cart": cart,
                "product": product,
                "products_num": 1,
            }
            cart_models.ShoppingCartItem.objects.create(**product_param)

        return Response({"details": "successfully added to cart"})


class CartView(generics.ListAPIView):
    serializer_class = CartDetailSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        try:
            user = self.request.user
            session_id = self.request.session._get_or_create_session_key()
            if user.is_anonymous:
                user = None
        except Exception as e:
            print(e)
            pass

        filter_params = {}
        if bool(user):
            filter_params.update({
                "user": user
            })
        else:
            filter_params.update({
                "session_id": session_id
            })

        cart = cart_models.ShoppingCart.objects.filter(
            **filter_params).first()
        if cart:
            cart_items = cart.cart_items.all().order_by('product')
            return cart_items
        return []
