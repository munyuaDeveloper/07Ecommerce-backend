from django.contrib import admin
from .models import ShoppingCart, ShoppingCartItem, OrderInfo, OrderProducts
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(OrderInfo)
admin.site.register(OrderProducts)
