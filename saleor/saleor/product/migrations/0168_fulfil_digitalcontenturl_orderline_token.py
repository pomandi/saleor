# Generated by Django 3.2.12 on 2022-04-12 14:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0167_digitalcontenturl_order_line_token"),
        ("order", "0140_alter_orderline_old_id_and_created_at"),
    ]

    operations = [
        migrations.RunSQL(
            """
            UPDATE product_digitalcontenturl
            SET order_line_token = (
                SELECT token
                FROM order_orderline
                WHERE product_digitalcontenturl.line_id = order_orderline.id
            )
            WHERE line_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
