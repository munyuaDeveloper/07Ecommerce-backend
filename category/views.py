from category.serializers import (
    ListCategorySerializer, CategoryCreateSerializer,
    ListCategoryProductSerializer)
from category.models import Category
from rest_framework import generics


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ListCategorySerializer


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class ListCategoryItemView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ListCategoryProductSerializer
