# Generated by Django 3.2.20 on 2023-08-16 12:14

from django.contrib.postgres.operations import RemoveIndexConcurrently
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("payment", "0051_alter_transactionitem_available_actions"),
    ]

    operations = [
        RemoveIndexConcurrently(
            model_name="transactionitem",
            name="payment_tra_order_i_e783c4_gin",
        )
    ]
