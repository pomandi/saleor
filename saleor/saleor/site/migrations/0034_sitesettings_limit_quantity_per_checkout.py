# Generated by Django 3.2.7 on 2021-10-21 14:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("site", "0033_sitesettings_reserve_stock_duration_minutes"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="limit_quantity_per_checkout",
            field=models.IntegerField(
                blank=True,
                default=50,
                null=True,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]
