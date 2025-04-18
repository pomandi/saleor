# Generated by Django 2.2.1 on 2019-06-11 11:49

import django.contrib.postgres.fields.jsonb
from django.db import migrations

import saleor.core.utils.json_serializer


class Migration(migrations.Migration):
    dependencies = [("shipping", "0015_auto_20190305_0640")]

    operations = [
        migrations.AddField(
            model_name="shippingmethod",
            name="meta",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
            ),
        )
    ]
