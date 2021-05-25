from django.conf.urls import url

from cart.views import AddToCartView, CartView, RemoveFromCartView, DeleteCartItemView

urlpatterns = [
    url(r'^add-cart/$', AddToCartView.as_view(), name='add-cart'),
    url(r'^remove-item/$', RemoveFromCartView.as_view(), name='remove-item'),
    url(r'^delete-cart/$', DeleteCartItemView.as_view(), name='delete-cart'),
    url(r'^cart/$', CartView.as_view(), name='cart')
]
