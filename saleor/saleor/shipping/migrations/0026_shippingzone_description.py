# Generated by Django 3.1.4 on 2020-12-29 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shipping", "0025_auto_20201130_1122"),
    ]

    operations = [
        migrations.AddField(
            model_name="shippingzone",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
