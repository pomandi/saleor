# Generated by Django 3.2.12 on 2022-03-07 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0135_alter_order_options"),
        ("giftcard", "0012_auto_20211007_0655"),
    ]

    operations = [
        migrations.AddField(
            model_name="giftcardevent",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="order.order",
            ),
        ),
    ]
