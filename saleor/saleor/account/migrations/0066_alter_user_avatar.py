# Generated by Django 3.2.13 on 2022-06-10 07:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0065_address_warehouse_address_search_gin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="user-avatars"),
        ),
    ]
