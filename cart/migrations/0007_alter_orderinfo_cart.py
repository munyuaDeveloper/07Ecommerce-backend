# Generated by Django 3.2.3 on 2021-05-25 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_auto_20210525_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.shoppingcart', verbose_name='cart'),
        ),
    ]