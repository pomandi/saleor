# Generated by Django 3.2.16 on 2022-12-08 09:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("channel", "0005_channel_allocation_strategy"),
    ]

    operations = [
        migrations.AddField(
            model_name="channel",
            name="automatically_confirm_all_new_orders",
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name="channel",
            name="automatically_fulfill_non_shippable_gift_card",
            field=models.BooleanField(default=True, null=True),
        ),
    ]
