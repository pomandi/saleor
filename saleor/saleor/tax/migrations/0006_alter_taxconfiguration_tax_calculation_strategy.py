# Generated by Django 3.2.16 on 2022-12-01 15:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tax", "0005_migrate_vatlayer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taxconfiguration",
            name="tax_calculation_strategy",
            field=models.CharField(
                blank=True,
                choices=[("FLAT_RATES", "Flat rates"), ("TAX_APP", "Tax app")],
                default="FLAT_RATES",
                max_length=20,
                null=True,
            ),
        ),
    ]
