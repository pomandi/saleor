# Generated by Django 1.9.1 on 2016-02-07 11:34

import datetime
import os

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("discount", "0002_voucher")]

    operations = [
        migrations.AlterField(
            model_name="sale",
            name="type",
            field=models.CharField(
                choices=[
                    ("fixed", os.environ.get("DEFAULT_CURRENCY", "USD")),
                    ("percentage", "%"),
                ],
                default="fixed",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="voucher",
            name="code",
            field=models.CharField(
                db_index=True, max_length=12, unique=True, verbose_name="code"
            ),
        ),
        migrations.AlterField(
            model_name="voucher",
            name="discount_value",
            field=models.DecimalField(
                decimal_places=2, max_digits=12, verbose_name="discount value"
            ),
        ),
        migrations.AlterField(
            model_name="voucher",
            name="discount_value_type",
            field=models.CharField(
                choices=[
                    ("fixed", os.environ.get("DEFAULT_CURRENCY", "USD")),
                    ("percentage", "%"),
                ],
                default="fixed",
                max_length=10,
                verbose_name="discount type",
            ),
        ),
        migrations.AlterField(
            model_name="voucher",
            name="end_date",
            field=models.DateField(blank=True, null=True, verbose_name="end date"),
        ),
        migrations.AlterField(
            model_name="voucher",
            name="name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="voucher",
            name="start_date",
            field=models.DateField(
                default=datetime.date.today, verbose_name="start date"
            ),
        ),
        migrations.AlterField(
            model_name="voucher",
            name="type",
            field=models.CharField(
                choices=[
                    ("value", "All purchases"),
                    ("product", "One product"),
                    ("category", "A category of products"),
                    ("shipping", "Shipping"),
                ],
                default="value",
                max_length=20,
                verbose_name="discount for",
            ),
        ),
        migrations.AlterField(
            model_name="voucher",
            name="usage_limit",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="usage limit"
            ),
        ),
    ]
