from django.conf.urls import url

from cart.views import AddToCart, CartView

urlpatterns = [
    url(r'^add-cart/$', AddToCart.as_view(), name='add-cart'),
    url(r'^cart/$', CartView.as_view(), name='cart')
]
