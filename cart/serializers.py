from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class AddToCartSerializer(serializers.Serializer):
    product = serializers.CharField()
