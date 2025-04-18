# Generated by Django 3.2.21 on 2023-10-04 10:26

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.operations import AddIndexConcurrently
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("discount", "0061_basediscount_add_voucher_code"),
    ]

    operations = [
        AddIndexConcurrently(
            model_name="orderdiscount",
            index=GinIndex(
                fields=["voucher_code"], name="orderdiscount_voucher_code_idx"
            ),
        ),
        AddIndexConcurrently(
            model_name="checkoutlinediscount",
            index=GinIndex(
                fields=["voucher_code"], name="checklinedisc_voucher_code_idx"
            ),
        ),
        AddIndexConcurrently(
            model_name="orderlinediscount",
            index=GinIndex(
                fields=["voucher_code"], name="orderlinedisc_voucher_code_idx"
            ),
        ),
    ]
