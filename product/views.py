from rest_framework import generics, permissions, filters
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductListSerializer, ProductCreateSerializer
from .models import Product


from users.models import CustomUser
from product.models import Product, ProductImage
from category.models import Category


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category__name']
    queryset = Product.objects.all().order_by('title')


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request):
        payload = request.data
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)

        user = request.user
        title = serializer.validated_data.get('title')
        desc = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        quantity = serializer.validated_data.get('quantity')
        images = serializer.validated_data.get('images')
        category = serializer.validated_data.get('category')

        category_query = Category.objects.filter(name=category).first()

        product_params = {
            "title": title,
            "description": desc,
            "price": price,
            "quantity": quantity,
            "seller": user
        }
        product_inst = Product.objects.create(**product_params)
        product_inst.category.add(category_query)
        product_inst.save()

        for image in images:
            image_param = {
                "image": image
            }
            image_inst, created = ProductImage.objects.get_or_create(
                **image_param)
            image_inst.product.add(product_inst)
            image_inst.save()

        product_details = ProductListSerializer(product_inst, many=False).data
        return Response(product_details)
