from django.contrib import admin
from .models import ShoppingCart, OrderInfo, OrderProducts
admin.site.register(ShoppingCart)
admin.site.register(OrderInfo)
admin.site.register(OrderProducts)