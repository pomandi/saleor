# Generated by Django 3.2.22 on 2024-05-22 09:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0172_update_order_cc_addresses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderline",
            name="unit_discount_type",
            field=models.CharField(
                blank=True,
                choices=[("fixed", "fixed"), ("percentage", "%")],
                max_length=10,
                null=True,
            ),
        ),
        migrations.RunSQL(
            """
            ALTER TABLE order_orderline
            ALTER COLUMN unit_discount_type
            SET DEFAULT null;
            """,
            migrations.RunSQL.noop,
        ),
        migrations.AddField(
            model_name="orderline",
            name="is_price_overridden",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
