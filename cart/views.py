from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartUnit
from cart.serializers import CartUnitSerializer


class CartView(APIView):
    pass


class CartUnitView(APIView):
    pass