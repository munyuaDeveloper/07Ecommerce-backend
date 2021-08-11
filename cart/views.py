from django.contrib.sessions.models import Session
from rest_framework import status, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import F, Count, Q

from cart import models as cart_models
from cart.serializers import (
    AddToCartSerializer, ListCartDetailSerializer, ListWishListDetailSerializer,
    OrderCreateSerializer, OrderDetailSerializer, GenericRequestSerializer
)

from product.models import Product

from shared_functions import utility_functions


class AddToCartView(generics.CreateAPIView):
    queryset = cart_models.ShoppingCart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = (AllowAny, )

    def create(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                user = None
                if request.session.session_key is None:
                    request.session.save()
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
                "user": user,
                "cart_status": "ON_DISPLAY"
            })
        else:
            cart_params.update({
                "session_id": request.session.session_key,
                "cart_status": "ON_DISPLAY"
            })
        cart = cart_models.ShoppingCart.objects.filter(**cart_params).first()
        if not bool(cart):
            cart = cart_models.ShoppingCart.objects.create(**cart_params)

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"details": "Sorry. Product does not exist"})

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
    serializer_class = GenericRequestSerializer
    permission_classes = (AllowAny, )

    def put(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                user = None
                if request.session.session_key is None:
                    request.session.save()
        except Exception as e:
            print(e)
            pass

        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        product_id = payload['request_id']

        cart_params = {}
        if bool(user):
            cart_params.update({
                "user": user,
                "cart_status": "ON_DISPLAY"
            })
        else:
            cart_params.update({
                "session_id": request.session.session_key,
                "cart_status": "ON_DISPLAY"
            })

        cart = cart_models.ShoppingCart.objects.filter(
            **cart_params).first()
        if not cart:
            return Response({"details": "Sorry. Cart does not exist"})

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"details": "Sorry. Product does not exist"})
        update_product = cart_models.ShoppingCartItem.objects.filter(
            cart=cart, product=product).first()
        if not update_product:
            return Response({"details": "Sorry. Cart does not exist"})
        item_count = update_product.products_num
        update_product.products_num = item_count - 1
        update_product.save(update_fields=['products_num'])

        item_count = update_product.products_num
        if item_count <= 0:
            update_product.delete()

        return Response({"details": "successfully updated"})


class DeleteCartItemView(generics.CreateAPIView):
    queryset = cart_models.ShoppingCart.objects.all()
    serializer_class = GenericRequestSerializer
    permission_classes = (AllowAny, )

    def create(self, request):
        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        product_id = payload['request_id']

        try:
            user = self.request.user
            if user.is_anonymous:
                user = None
                if request.session.session_key is None:
                    request.session.save()
        except Exception as e:
            print(e)
            pass

        query = Q()
        if bool(user):
            query.add(Q(cart__user=user, id=product_id,
                      cart__cart_status="ON_DISPLAY"), Q.AND)
        else:
            query.add(Q(cart__session_id=request.session.session_key,
                        id=product_id, cart__cart_status="ON_DISPLAY"), Q.AND)

        update_product = cart_models.ShoppingCartItem.objects.filter(
            query).first()
        if not update_product:
            return Response({"details": "cart does not exist"})

        update_product.delete()
        return Response({"details": "successfully deleted"})


class CartView(generics.ListAPIView):
    serializer_class = ListCartDetailSerializer
    permission_classes = (AllowAny, )
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'cart_status',
        'cart_items__product__title',
        'cart_items__product__description',
        'cart_items__product__category__name']

    def get_queryset(self):
        try:
            user = self.request.user
            if user.is_anonymous:
                user = None
                if self.request.session.session_key is None:
                    self.request.session.save()
        except Exception as e:
            print(e)
            pass

        filter_params = {}
        if bool(user):
            filter_params.update({
                "user": user,
                "cart_status": "ON_DISPLAY"
            })
        else:
            filter_params.update({
                "session_id": self.request.session.session_key,
                "cart_status": "ON_DISPLAY"
            })

        cart = cart_models.ShoppingCart.objects.filter(
            **filter_params).order_by('-date_created')
        return cart


class CreateOrderView(generics.CreateAPIView):
    queryset = cart_models.OrderInfo.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (AllowAny, )

    def create(self, request):
        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        reference_number = utility_functions.generate_unique_reference_per_model(
            cart_models.OrderInfo, size=6)
        location = payload['pickup_location']
        phone_number = payload['phone_number']
        email = payload['email']
        cart_id = payload['cart']
        method_of_payment = payload['method_of_payment']
        card_owner = payload['card_owner']
        card_number = payload['card_number']
        card_cvc = payload['card_cvc']

        cart_inst = cart_models.ShoppingCart.objects.filter(
            id=cart_id, cart_status="ON_DISPLAY").first()
        if not cart_inst:
            return Response({"details": "Kindly create shopping cart"})

        cart_items = cart_inst.cart_items.all()
        total_amts = 0
        for item in cart_items:
            product = item.product
            quantity = item.products_num
            price = product.price
            total_amts += (quantity * price)

        order_params = {
            "cart": cart_inst,
            "payment_status": "WAIT_BUYER_PAY",
            "order_status": "ONGOING",
            "pickup_location": location,
            "phone_number": phone_number,
            "email": email,
            "method_of_payment": method_of_payment,
            "card_owner": card_owner,
            "card_number": card_number,
            "card_cvc": card_cvc,
        }
        order_inst, created = cart_models.OrderInfo.objects.get_or_create(
            **order_params)

        if not created:
            reference_number = order_inst.order_reference

        order_inst.order_mount = total_amts
        order_inst.order_reference = reference_number
        order_inst.save(update_fields=['order_mount', 'order_reference'])

        cart_inst.cart_status = 'ONGOING'
        cart_inst.save(update_fields=['cart_status'])

        order_details = OrderDetailSerializer(order_inst, many=False).data
        return Response(order_details)


class ListOrderView(generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = (AllowAny, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['order_reference', 'payment_status']

    def get_queryset(self):
        try:
            user = self.request.user
            if user.is_anonymous:
                user = None
                if self.request.session.session_key is None:
                    self.request.session.save()
        except Exception as e:
            print(e)
            pass

        order_status = self.request.query_params.get('filter', None)
        if not bool(order_status):
            order_status = "ONGOING"

        allowed_status = ["ONGOING", "COMPLETE", ]
        if order_status.upper() not in allowed_status:
            return []

        query = Q()
        if bool(user):
            query.add(Q(cart__user=user,
                        cart__cart_status__iexact=order_status), Q.AND)
        else:
            query.add(Q(cart__session_id=self.request.session.session_key,
                      cart__cart_status__iexact=order_status), Q.AND)

        order_queryset = cart_models.OrderInfo.objects.filter(
            query).order_by('-date_created')
        return order_queryset


class UpdateOrderView(generics.UpdateAPIView):
    serializer_class = GenericRequestSerializer
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        product_id = payload['request_id']
        try:
            order_queryset = cart_models.OrderInfo.objects.get(
                id=product_id)
        except Exception as e:
            return Response({"details": "Order does not exist"})

        if order_queryset.cart.cart_status != "ONGOING":
            return Response({"details": "Order is already completed"})

        order_queryset.payment_status = "TRADE_CLOSED"
        order_queryset.order_status = "COMPLETE"
        order_queryset.save(update_fields=['payment_status'])

        cart = order_queryset.cart
        cart.cart_status = "COMPLETE"
        cart.save(update_fields=['cart_status'])
        return Response({"details": "successfully updated"})


class AddToWishListView(generics.CreateAPIView):
    queryset = cart_models.WishList.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = (AllowAny, )

    def create(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                user = None
                if request.session.session_key is None:
                    request.session.save()
        except Exception as e:
            print(e)
            pass

        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        product_id = payload['product']

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"details": "Sorry. Product does not exist"})

        wish_params = {
            "product": product
        }
        if bool(user):
            wish_params.update({
                "user": user
            })
        else:
            wish_params.update({
                "session_id": request.session.session_key
            })
        wish_list = cart_models.WishList.objects.filter(**wish_params).first()
        if not bool(wish_list):
            cart = cart_models.WishList.objects.create(**wish_params)

        return Response({"details": "successfully added to wish list"})


class RemoveFromWishListView(generics.DestroyAPIView):
    queryset = cart_models.WishList.objects.all()
    serializer_class = GenericRequestSerializer
    permission_classes = (AllowAny, )

    def delete(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                user = None
                if request.session.session_key is None:
                    request.session.save()
        except Exception as e:
            print(e)
            pass

        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        wish_id = payload['request_id']
        try:
            wish_list = cart_models.WishList.objects.get(id=wish_id)
        except Exception as e:
            print(e)
            return Response({"details": "Sorry. Wish list item does not exist"})

        session_id = self.request.session.session_key,
        if wish_list.user != user:
            if wish_list.session_id != user:
                return Response({"details": "Unable to remove item from wish list"})

        wish_list.delete()
        return Response({"details": "successfully removed item from wish list"})


class WishListView(generics.ListAPIView):
    serializer_class = ListWishListDetailSerializer
    permission_classes = (AllowAny, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__title',
                     'product__description', 'product__category__name']

    def get_queryset(self):
        try:
            user = self.request.user
            if user.is_anonymous:
                user = None
                if self.request.session.session_key is None:
                    self.request.session.save()
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
                "session_id": self.request.session.session_key
            })

        wish_list = cart_models.WishList.objects.filter(
            **filter_params).order_by('-date_created')
        return wish_list
