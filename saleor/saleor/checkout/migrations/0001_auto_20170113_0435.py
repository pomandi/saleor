# Generated by Django 1.10.3 on 2017-01-13 10:35

from django.contrib.postgres import fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("checkout", "fix_empty_data_in_lines")]

    replaces = [("cart", "0001_auto_20170113_0435")]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="checkout_data",
            field=fields.JSONField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="cartline",
            name="data",
            field=fields.JSONField(blank=True, default=dict),
        ),
    ]
