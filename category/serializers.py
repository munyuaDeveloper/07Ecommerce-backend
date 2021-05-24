from category.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    model = Category
    fields = ['name']

    def to_representation(self, instance):
        return instance.name