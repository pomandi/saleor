# Generated by Django 3.2.13 on 2022-05-16 07:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0146_merge_20220512_1005"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="orderline",
            options={"ordering": ("created_at", "id")},
        ),
    ]
