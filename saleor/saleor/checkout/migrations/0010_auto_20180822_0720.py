# Generated by Django 2.0.3 on 2018-08-22 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("checkout", "0009_cart_translated_discount_name")]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="shipping_method",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="carts",
                to="shipping.ShippingMethod",
            ),
        )
    ]
