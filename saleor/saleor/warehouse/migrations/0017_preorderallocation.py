# Generated by Django 3.2.7 on 2021-10-01 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0150_auto_20211001_1004"),
        ("order", "0120_orderline_optional_sku"),
        ("warehouse", "0016_merge_20210921_1036"),
    ]

    operations = [
        migrations.CreateModel(
            name="PreorderAllocation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=0)),
                (
                    "order_line",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preorder_allocations",
                        to="order.orderline",
                    ),
                ),
                (
                    "product_variant_channel_listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preorder_allocations",
                        to="product.productvariantchannellisting",
                    ),
                ),
            ],
            options={
                "ordering": ("pk",),
                "unique_together": {("order_line", "product_variant_channel_listing")},
            },
        ),
    ]
