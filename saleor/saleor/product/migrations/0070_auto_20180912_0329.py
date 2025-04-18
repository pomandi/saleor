# Generated by Django 2.1.1 on 2018-09-12 08:29

import django.contrib.postgres.fields.hstore
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("product", "0069_auto_20180912_0326")]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="attributes",
            field=django.contrib.postgres.fields.hstore.HStoreField(
                blank=True, default=dict
            ),
        ),
        migrations.AlterField(
            model_name="productvariant",
            name="attributes",
            field=django.contrib.postgres.fields.hstore.HStoreField(
                blank=True, default=dict
            ),
        ),
    ]
