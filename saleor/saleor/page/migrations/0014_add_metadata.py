# Generated by Django 3.1.2 on 2020-10-20 09:48

from django.db import migrations, models

import saleor.core.utils.json_serializer


class Migration(migrations.Migration):
    dependencies = [
        ("page", "0013_update_publication_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="metadata",
            field=models.JSONField(
                blank=True,
                default=dict,
                encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="private_metadata",
            field=models.JSONField(
                blank=True,
                default=dict,
                encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                null=True,
            ),
        ),
    ]
