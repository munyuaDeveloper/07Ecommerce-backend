from django.db import models

from category.models import Category
from users.models import CustomUser


class Product(models.Model):
    category = models.ManyToManyField(
        to=Category, related_name='categories', blank=True)
    seller = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    num_in_stock = models.PositiveIntegerField(default=5)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.id} -- {self.title}"

    @property
    def num_in_stock(self):
        return Product.objects.filter(title=self.title).all().count()


class ProductImage(models.Model):
    product = models.ManyToManyField(
        to=Product, blank=True, related_name='product_image')
    image = models.CharField(max_length=255)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['image']

    def __str__(self):
        product = self.product.first()
        if product is not None:
            product_title = product.title
        else:
            product_title = 'No product assigned'

        return '{}: {}'.format(product_title)

    def delete(self, *args, **kwargs):
        self.image.delete()

        super(ProductImage, self).delete(*args, **kwargs)
