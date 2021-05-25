from django.db.models.base import Model
from django.http.response import ResponseHeaders
from category.serializers import CategorySerializer
from category.models import Category
from rest_framework import generics, response, status



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(generics.CreateAPIView):
    pass
