# Generated by Django 3.2.12 on 2022-02-09 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0158_auto_20220120_1633"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="created",
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="productvariant",
            name="created",
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="productvariant",
            name="updated_at",
            field=models.DateTimeField(db_index=True, null=True),
        ),
    ]
