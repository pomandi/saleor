# Generated by Django 3.2.12 on 2022-02-24 08:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0129_alter_order_number"),
        ("account", "0062_alter_user_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerevent",
            name="order_token",
            field=models.UUIDField(null=True),
        ),
        migrations.RunSQL(
            """
            UPDATE account_customerevent
            SET order_token = (
                SELECT token
                FROM order_order
                WHERE account_customerevent.order_id = order_order.id
            )
            WHERE order_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AlterField(
            model_name="customerevent",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="order.order",
                to_field="number",
            ),
        ),
    ]
