from django.contrib import admin

from order.models import Order
from order_unit.models import OrderUnit
from product.models import Product
from property.models import PropertyValue, Property
from category.models import Category
from unit.models import Unit, UnitImage
from users.models import CustomUser
from .admin_models import UnitAdmin, ProductAdmin, UnitImageAdmin, OrderAdmin, OrderUnitAdmin, PropertyAdmin, \
    PropertyValueAdmin

admin.site.register([CustomUser,
                     Category])

admin.site.register(PropertyValue, PropertyValueAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UnitImage, UnitImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUnit, OrderUnitAdmin)
