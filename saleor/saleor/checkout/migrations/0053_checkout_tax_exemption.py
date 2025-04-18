# Generated by Django 3.2.14 on 2022-08-03 09:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0052_alter_checkoutline_currency"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkout",
            name="tax_exemption",
            field=models.BooleanField(default=False),
        ),
        migrations.RunSQL(
            """
            ALTER TABLE checkout_checkout ALTER COLUMN tax_exemption SET DEFAULT
            false;
            """,
            migrations.RunSQL.noop,
        ),
    ]
