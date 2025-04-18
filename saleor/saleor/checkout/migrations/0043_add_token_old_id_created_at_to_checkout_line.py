# Generated by Django 3.2.13 on 2022-04-29 08:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0042_rename_created_checkout_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkoutline",
            name="created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="checkoutline",
            name="old_id",
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="checkoutline",
            name="token",
            field=models.UUIDField(null=True, unique=True),
        ),
    ]
