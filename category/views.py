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
    serializer_class = ListCategoryProductSerializer

    def get_queryset(self):
        request_id = self.request.query_params.get('request_id', None)
        if not bool(request_id):
            return []

        queryset = Category.objects.filter(id=request_id).order_by('id')
        return queryset
