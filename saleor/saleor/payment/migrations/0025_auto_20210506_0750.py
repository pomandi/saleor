# Generated by Django 3.1.8 on 2021-05-06 07:50

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0024_auto_20210326_0837"),
    ]

    operations = [
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="payment",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["order_id", "is_active", "charge_status"],
                name="payment_pay_order_i_f22aa2_gin",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="searchable_key",
            field=models.CharField(
                blank=True, db_index=True, max_length=512, null=True
            ),
        ),
    ]
