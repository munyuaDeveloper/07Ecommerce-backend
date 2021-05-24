from django.db import models
# from unit.models import Unit
# from order_unit.models import OrderUnit

from django.contrib.auth import get_user_model as user_model
User = user_model()


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # unit_set = models.ManyToManyField(to=Unit, through='OrderUnit')
    user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=31)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        items_count = self.unit_set.all().count()
        return 'Order ({} items) by {}'.format(items_count, self.name)
