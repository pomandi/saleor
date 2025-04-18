# Generated by Django 3.2.12 on 2022-04-12 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse", "0022_fulfil_allocation_order_line_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="allocation",
            name="order_line",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="allocations",
                to="order.orderline",
                to_field="old_id",
            ),
        ),
        migrations.AlterField(
            model_name="preorderallocation",
            name="order_line",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="preorder_allocations",
                to="order.orderline",
                to_field="old_id",
            ),
        ),
    ]
