# Generated by Django 3.2.13 on 2022-04-29 09:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse", "0025_add_checkout_line_token"),
        ("checkout", "0044_fulfill_checkout_line_new_fields"),
    ]

    operations = [
        migrations.RunSQL(
            """
            UPDATE warehouse_preorderreservation
            SET checkout_line_token = (
                SELECT token
                FROM checkout_checkoutline
                WHERE (
                    warehouse_preorderreservation.checkout_line_id
                    = checkout_checkoutline.id
                )
            )
            WHERE checkout_line_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            """
            UPDATE warehouse_reservation
            SET checkout_line_token = (
                SELECT token
                FROM checkout_checkoutline
                WHERE (
                    warehouse_reservation.checkout_line_id
                    = checkout_checkoutline.id
                )
            )
            WHERE checkout_line_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
