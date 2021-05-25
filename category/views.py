from category.serializers import ListCategorySerializer, CategoryCreateSerializer
from category.models import Category
from rest_framework import generics, response, status


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ListCategorySerializer


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
