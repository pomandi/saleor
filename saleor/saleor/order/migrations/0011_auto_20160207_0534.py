# Generated by Django 1.9.1 on 2016-02-07 11:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("discount", "0003_auto_20160207_0534"),
        ("order", "0010_auto_20160119_0541"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="discount_amount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=12, null=True
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="discount_name",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="order",
            name="voucher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="discount.Voucher",
            ),
        ),
    ]
