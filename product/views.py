from rest_framework import generics, permissions

from product.models import Product
from product.serializers import ProductListSerializer, ProductCreateSerializer
from .models import Product


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        q = self.request.query_params.get('q', None)
        category = self.request.query_params.get('category')

        if q is not None:
            queryset = queryset.filter(title__icontains=q)

        if category:
            category = category.split(',')

            for cat in category:
                queryset = queryset.filter(
                    cat_set__name__iexact=cat).distinct()

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )
