# Generated by Django 3.2.5 on 2021-07-13 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0148_producttype_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productvariant",
            name="sku",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
