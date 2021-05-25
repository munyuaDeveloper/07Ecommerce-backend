from django.contrib.sessions.models import Session
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cart import models as cart_models
from cart.serializers import AddToCartSerializer


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

        cart_params = {
            "session_id": session_id
        }

        return Response("success")


class CartView(APIView):
    pass


class CartUnitView(APIView):
    pass
