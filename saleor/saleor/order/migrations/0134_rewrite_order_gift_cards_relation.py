# Generated by Django 3.2.12 on 2022-02-28 12:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0133_rename_order_token_id"),
    ]

    operations = [
        # rewrite order - gift cards relation - all operations are performed on
        # order_order_gift_cards table which is responsible for order-gift cards
        # many to many relation
        #   - add fk constraint to order id
        #   - delete constraint to order number
        #   - delete order_id column
        #   - rename order_token to order_id
        #   - rename newly added constraint
        migrations.RunSQL(
            """
            ALTER TABLE order_order_gift_cards
                ADD CONSTRAINT order_order_gift_cards_order_token_fk_order_order_id
                FOREIGN KEY (order_token) REFERENCES order_order (id);

            ALTER TABLE order_order_gift_cards
            DROP CONSTRAINT order_order_gift_cards_order_id_fk_order_order_number;

            ALTER TABLE order_order_gift_cards
            DROP COLUMN order_id;

            ALTER TABLE order_order_gift_cards
            RENAME COLUMN order_token TO order_id;

            ALTER TABLE order_order_gift_cards
            RENAME CONSTRAINT order_order_gift_cards_order_token_fk_order_order_id
            TO order_order_gift_cards_order_id_ce5608c4_fk_order_order_id;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
