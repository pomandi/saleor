# Generated by Django 3.2.12 on 2022-04-12 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0141_fulfil_fulfillmentline_orderline_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fulfillmentline",
            name="order_line",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fulfillment_lines",
                to="order.orderline",
                to_field="old_id",
            ),
        ),
    ]
