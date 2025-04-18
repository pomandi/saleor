# Generated by Django 3.2.12 on 2022-04-12 09:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse", "0021_allocation_order_line_token"),
        ("order", "0140_alter_orderline_old_id_and_created_at"),
    ]

    operations = [
        migrations.RunSQL(
            """
            UPDATE warehouse_allocation
            SET order_line_token = (
                SELECT token
                FROM order_orderline
                WHERE warehouse_allocation.order_line_id = order_orderline.id
            )
            WHERE order_line_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            """
            UPDATE warehouse_preorderallocation
            SET order_line_token = (
                SELECT token
                FROM order_orderline
                WHERE warehouse_preorderallocation.order_line_id = order_orderline.id
            )
            WHERE order_line_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
