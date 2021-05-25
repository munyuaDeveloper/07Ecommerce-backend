from django.conf.urls import url

from cart import views

urlpatterns = [
    url(r'^add-cart/$', views.AddToCartView.as_view(), name='add-cart'),
    url(r'^remove-item/$', views.RemoveFromCartView.as_view(), name='remove-item'),
    url(r'^delete-cart/$', views.DeleteCartItemView.as_view(), name='delete-cart'),
    url(r'^cart/$', views.CartView.as_view(), name='cart'),

    url(r'^create-order/$', views.CreateOrderView.as_view(), name='create-order'),
    url(r'^list-order/$', views.ListOrderView.as_view(), name='list-order'),
    url(r'^update-order/$', views.UpdateOrderView.as_view(), name='update-order'),

]
