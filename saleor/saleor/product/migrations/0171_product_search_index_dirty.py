# Generated by Django 3.2.14 on 2022-07-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0170_rewrite_digitalcontenturl_orderline_relation"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="search_index_dirty",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="search_index_dirty",
            field=models.BooleanField(default=False),
        ),
    ]
