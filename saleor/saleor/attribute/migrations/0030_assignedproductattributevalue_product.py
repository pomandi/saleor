# Generated by Django 3.2.20 on 2023-08-23 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0186_remove_product_charge_taxes"),
        ("attribute", "0029_alter_attribute_unit"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignedproductattributevalue",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attributevalues",
                to="product.product",
                db_index=False,
            ),
        ),
    ]
