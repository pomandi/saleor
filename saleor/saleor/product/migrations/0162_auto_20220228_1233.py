# Generated by Django 3.2.12 on 2022-02-28 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0161_auto_20220209_1511"),
    ]

    operations = [
        migrations.AddField(
            model_name="productmedia",
            name="to_remove",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="productmedia",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="media",
                to="product.product",
            ),
        ),
    ]
