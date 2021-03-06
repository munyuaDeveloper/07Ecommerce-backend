from django.contrib import admin
from .models import ShoppingCart, ShoppingCartItem, OrderInfo, WishList


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('order_status',)
    search_fields = [
        'order_status__iexact', 'order_reference', 'payment_status', 'order_mount']


admin.site.register(OrderInfo, OrderAdmin)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(WishList)
