# Generated by Django 1.9.1 on 2016-01-14 10:19

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("account", "0003_auto_20151104_1102")]

    replaces = [("userprofile", "0004_auto_20160114_0419")]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="country",
            field=django_countries.fields.CountryField(
                max_length=2, verbose_name="country"
            ),
        )
    ]
