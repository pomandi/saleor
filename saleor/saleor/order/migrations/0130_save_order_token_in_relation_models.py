# Generated by Django 3.2.12 on 2022-02-24 14:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0129_alter_order_number"),
    ]

    operations = [
        # update Fulfillment model
        migrations.AddField(
            model_name="fulfillment",
            name="order_token",
            field=models.UUIDField(null=True),
        ),
        migrations.RunSQL(
            """
            UPDATE order_fulfillment
            SET order_token = (
                SELECT token
                FROM order_order
                WHERE order_fulfillment.order_id = order_order.id
            )
            WHERE order_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AlterField(
            model_name="fulfillment",
            name="order",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fulfillments",
                to="order.order",
                to_field="number",
            ),
        ),
        # update OrderEvent model
        migrations.AddField(
            model_name="orderevent",
            name="order_token",
            field=models.UUIDField(null=True),
        ),
        migrations.RunSQL(
            """
            UPDATE order_orderevent
            SET order_token = (
                SELECT token
                FROM order_order
                WHERE order_orderevent.order_id = order_order.id
            )
            WHERE order_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AlterField(
            model_name="orderevent",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="order.order",
                to_field="number",
            ),
        ),
        # update OrderLine model
        migrations.AddField(
            model_name="orderline",
            name="order_token",
            field=models.UUIDField(null=True),
        ),
        migrations.RunSQL(
            """
            UPDATE order_orderline
            SET order_token = (
                SELECT token
                FROM order_order
                WHERE order_orderline.order_id = order_order.id
            )
            WHERE order_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AlterField(
            model_name="orderline",
            name="order",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lines",
                to="order.order",
                to_field="number",
            ),
        ),
        # update Order model
        migrations.AddField(
            model_name="order",
            name="original_token",
            field=models.UUIDField(null=True),
        ),
        migrations.RunSQL(
            """
            UPDATE order_order
            SET original_token = (
                SELECT token
                FROM order_order
                WHERE order_order.original_id = order_order.id
            )
            WHERE original_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AlterField(
            model_name="order",
            name="original",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="order.order",
                to_field="number",
            ),
        ),
        # drop many to many gift cards relation to order id
        # add relation to order number instead and add order token column
        #   - add order_token column
        #   - fill order_token with corresponding order token values
        #   - remove constraint that uses order id
        #   - add constraint to order number field
        migrations.RunSQL(
            """
            ALTER TABLE order_order_gift_cards
            ADD COLUMN order_token uuid;

            UPDATE order_order_gift_cards
            SET order_token = (
                SELECT token
                FROM order_order
                WHERE order_order_gift_cards.order_id = order_order.id
            );

            ALTER TABLE order_order_gift_cards
            ALTER COLUMN order_token SET NOT NULL;

            ALTER TABLE order_order_gift_cards
                DROP CONSTRAINT
                    order_order_gift_cards_order_id_ce5608c4_fk_order_order_id;

            ALTER TABLE order_order_gift_cards
                ADD CONSTRAINT order_order_gift_cards_order_id_fk_order_order_number
                FOREIGN KEY (order_id) REFERENCES order_order (number);

            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
