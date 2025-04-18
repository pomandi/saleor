# Generated by Django 3.2.23 on 2024-01-30 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0190_merge_20231221_1356"),
    ]

    operations = [
        migrations.AddField(
            model_name="productchannellisting",
            name="discounted_price_dirty",
            field=models.BooleanField(default=False),
        ),
        migrations.RunSQL(
            """
            ALTER TABLE product_productchannellisting
            ALTER COLUMN discounted_price_dirty
            SET DEFAULT false;
            """,
            migrations.RunSQL.noop,
        ),
    ]
