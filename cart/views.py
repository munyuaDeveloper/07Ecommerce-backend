from django.contrib.sessions.models import Session
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F, Count

from cart import models as cart_models
from cart.serializers import AddToCartSerializer, CartDetailSerializer, OrderCreateSerializer

from product.models import Product


class AddToCartView(generics.CreateAPIView):
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


class RemoveFromCartView(generics.UpdateAPIView):
    queryset = cart_models.ShoppingCart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = (AllowAny, )

    def put(self, request):
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
            cart=cart, product=product).first()
        if not update_product:
            return Response()
        item_count = update_product.products_num
        update_product.products_num = item_count - 1
        update_product.save(update_fields=['products_num'])

        item_count = update_product.products_num
        if item_count <= 0:
            update_product.delete()

        return Response({"details": "successfully updated"})


class DeleteCartItemView(generics.CreateAPIView):
    queryset = cart_models.ShoppingCart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = (AllowAny, )

    def create(self, request):
        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        product_id = payload['product']

        update_product = cart_models.ShoppingCartItem.objects.filter(
            id=product_id).first()
        if not update_product:
            return Response()

        update_product.delete()
        return Response({"details": "successfully deleted"})


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


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
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

        filter_params = {}
        if bool(user):
            filter_params.update({
                "user": user
            })
        else:
            filter_params.update({
                "session_id": session_id
            })
