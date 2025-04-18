# Generated by Django 2.0.8 on 2018-09-21 14:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("order", "0061_auto_20180920_0859")]

    operations = [
        migrations.AlterField(
            model_name="fulfillmentline",
            name="quantity",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="quantity",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="quantity_fulfilled",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]
