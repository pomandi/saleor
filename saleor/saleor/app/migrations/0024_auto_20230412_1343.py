# Generated by Django 3.2.18 on 2023-04-12 13:43

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0023_populate_app_and_app_installation_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="app",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name="appinstallation",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
