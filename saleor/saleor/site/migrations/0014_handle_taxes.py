# Generated by Django 2.0.3 on 2018-04-16 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("site", "0013_assign_default_menus")]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="display_gross_prices",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="include_taxes_in_prices",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="charge_taxes_on_shipping",
            field=models.BooleanField(default=True),
        ),
    ]
