# Generated by Django 3.2.6 on 2021-08-19 11:13

import django_countries.fields
from django.conf import settings
from django.db import migrations


def set_default_country_for_channels(apps, schema_editor):
    Warehouse = apps.get_model("warehouse", "Warehouse")
    Channel = apps.get_model("channel", "Channel")

    channels = Channel.objects.all()
    for channel in channels:
        # For each channel get the first available warehouse and use it's country code
        warehouse = Warehouse.objects.filter(
            shipping_zones__channels=channel.pk
        ).first()
        if warehouse and warehouse.address and warehouse.address.country:
            country = warehouse.address.country.code
        else:
            country = settings.DEFAULT_COUNTRY

        channel.default_country = country
        channel.save(update_fields=["default_country"])


class Migration(migrations.Migration):
    dependencies = [
        ("channel", "0002_channel_default_country"),
        ("shipping", "0029_shippingzone_channels"),
    ]

    operations = [
        migrations.RunPython(
            set_default_country_for_channels, reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="channel",
            name="default_country",
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
