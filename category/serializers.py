from category.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        name = validated_data.get('name')
        name = name.upper()
        category = Category.objects.filter(name__icontains=name)
        if category.exists():
            category = category.first()
            response = {
                "name": category.name
            }
            return response

        Category.objects.create(name=name)
        response = {
            "name": name
        }
        return response
