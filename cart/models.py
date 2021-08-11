from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()

CART_STATUS = [
    ("ON_DISPLAY", "ON_DISPLAY"),
    ("ONGOING", "ONGOING"),
    ("COMPLETE", "COMPLETE"),
]


class ShoppingCart(models.Model):
    """
         shopping cart 
    """
    user = models.ForeignKey(
        User, verbose_name=u"user",
        on_delete=models.CASCADE, null=True)
    session_id = models.CharField(max_length=255, null=True)
    cart_status = models.CharField(
        choices=CART_STATUS, max_length=30, verbose_name="Cart Status")
    date_created = models.DateTimeField(auto_now_add=True)

    # @property
    # def total(self):
    #     cart = ShoppingCart.objects.filter(
    #         Q(user=self.user) | Q(session_id=self.session_id)).first()
    #     print(cart)
    #     items = list(cart.cart_items.values_list("total", flat=True))
    #     print(items)
    #     return sum(items)

    def __str__(self):
        return f"{self.id}"


class ShoppingCartItem(models.Model):
    """
         shopping cart items
    """
    cart = models.ForeignKey(ShoppingCart, related_name='cart_items', null=True,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, verbose_name=u"commodity", on_delete=models.CASCADE, related_name='products')
    products_num = models.IntegerField(
        default=0, verbose_name="Number of Products")

    @property
    def total(self):
        total = self.products_num * self.product.price
        return total

    class Meta:
        verbose_name = "shopping cart Items"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.product.title} {self.products_num}"


class OrderInfo(models.Model):
    """
         order information 
    """
    PAYMENT_STATUS = (
        ("TRADE_SUCCESS", "success"),
        ("TRADE_CLOSED", "Timeout off"),
        ("WAIT_BUYER_PAY", "Transaction creation"),
        ("TRADE_FINISHED", "End of transaction"),
    )
    ORDER_STATUS = (
        ("ONGOING", "ONGOING"),
        ("COMPLETE", "COMPLETE")
    )

    cart = models.ForeignKey(ShoppingCart, verbose_name="cart",
                             null=True, on_delete=models.CASCADE)
    order_reference = models.CharField(
        max_length=30, null=True, blank=True, unique=True, verbose_name="order number")
    payment_status = models.CharField(
        choices=PAYMENT_STATUS, max_length=30, verbose_name="Payment Status")
    order_status = models.CharField(
        choices=ORDER_STATUS, max_length=30, blank=True, verbose_name="Order Status")
    order_mount = models.FloatField(default=0.0, verbose_name="order amount")

    # User Info
    pickup_location = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    method_of_payment = models.CharField(max_length=255, null=True)
    card_owner = models.CharField(max_length=255, null=True)
    card_number = models.CharField(max_length=255, null=True)
    card_cvc = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = u"order"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_reference)


class WishList(models.Model):
    """
         wish list products
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    session_id = models.CharField(max_length=255, null=True)
    product = models.ForeignKey(
        Product, verbose_name=u"commodity", on_delete=models.CASCADE,
        related_name='wish_product')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
