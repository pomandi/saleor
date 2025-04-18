# Generated by Django 3.2.12 on 2022-04-13 07:27

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0142_alter_fulfillmentline_line"),
        ("warehouse", "0023_alter_orderline_relations"),
        ("product", "0169_alter_digitalcontenturl_line"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderline",
            name="id",
        ),
        migrations.AlterField(
            model_name="orderline",
            name="token",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.RenameField(
            model_name="orderline",
            old_name="token",
            new_name="id",
        ),
        migrations.AlterModelOptions(
            name="orderline",
            options={"ordering": ("created_at",)},
        ),
    ]
