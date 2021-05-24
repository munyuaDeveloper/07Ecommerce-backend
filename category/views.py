from category.serializers import CategorySerializer
from category.models import Category
from rest_framework import generics



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
