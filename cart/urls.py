from django.conf.urls import url

from cart.views import AddToCart, CartView, CartUnitView

urlpatterns = [
    url(r'^add-cart/$', AddToCart.as_view(), name='add-cart'),
    url(r'^cart/$', AddToCart.as_view(), name='cart'),
    url(r'^cart/(?P<sku>[A-Za-z\-_0-9]+)/$',
        CartUnitView.as_view(), name='cart-unit'),
]
