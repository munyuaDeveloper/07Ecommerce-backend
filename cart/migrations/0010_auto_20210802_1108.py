# Generated by Django 3.2.3 on 2021-08-02 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_shoppingcart_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='card_cvc',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='card_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='card_owner',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='method_of_payment',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
