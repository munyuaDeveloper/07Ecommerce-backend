# Generated by Django 3.2.3 on 2021-05-24 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('num_in_stock', models.PositiveIntegerField(default=5)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('value_set', models.ManyToManyField(to='property.PropertyValue')),
            ],
            options={
                'ordering': ['product__title'],
            },
        ),
    ]
