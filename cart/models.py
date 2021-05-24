from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from datetime import datetime

User = get_user_model()

class ShoppingCart(models.Model):
    """
         shopping cart 
    """
    user = models.ForeignKey(User, verbose_name=u"user", on_delete=models.CASCADE)
    products = models.ForeignKey(Product, verbose_name=u"commodity", on_delete=models.CASCADE, related_name='products')
    nums = models.IntegerField(default=0, verbose_name="Number of purchases")

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"add time")

    class Meta:
        verbose_name = "shopping cart"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self.products.title, self.nums)


class OrderInfo(models.Model):
    """
         order information 
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "success"),
        ("TRADE_CLOSED", "Timeout off"),
        ("WAIT_BUYER_PAY", "Transaction creation"),
        ("TRADE_FINISHED", "End of transaction"),
        ("paying", "To be paid"),
    )
    # PAY_TYPE = (
    # ("alipay", "Alipay"),
    # ("wechat", "WeChat")
    # )

    user = models.ForeignKey(User, verbose_name="user", null=True, on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="order number")
    trade_no = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name=u"transaction number")
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="Order Status")
    post_script = models.CharField(max_length=200, verbose_name="Order Message")
    order_mount = models.FloatField(default=0.0, verbose_name="order amount")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="Payment time")

    # User Info
    address = models.CharField(max_length=100, default="", verbose_name="Shipping address")
    signer_name = models.CharField(max_length=20, default="", verbose_name="Signature")
    signer_mobile = models.CharField(max_length=11, verbose_name="contact number")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="add time")

    class Meta:
        verbose_name = u"order"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderProducts(models.Model):
    """
         Product details for the order
    """
    order = models.ForeignKey(OrderInfo, verbose_name="order information", related_name="goods", on_delete=models.CASCADE)
    products = models.ForeignKey(Product, verbose_name="commodity", on_delete=models.CASCADE)
    products_num = models.IntegerField(default=0, verbose_name="Number of Products")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="add time")

    class Meta:
        verbose_name = "Order products"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)