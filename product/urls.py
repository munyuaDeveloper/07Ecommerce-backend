from django.conf.urls import url
from django.urls.conf import path

from product.views import ProductListView, ProductDetailView, ProductCreateView

urlpatterns = [
    path('product-list', ProductListView.as_view(), name='product-list'),
    path('product-create', ProductCreateView.as_view(), name='product-create'),
    url(r'^product-details/(?P<pk>[0-9]+)/$',
        ProductDetailView.as_view(), name='product-detail'),
]
