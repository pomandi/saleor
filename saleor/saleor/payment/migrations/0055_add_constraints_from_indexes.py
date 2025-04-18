# Generated by Django 3.2.22 on 2023-12-11 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ("payment", "0054_add_idempotency_key_indexes"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                ALTER TABLE payment_transactionitem ADD CONSTRAINT
                unique_transaction_idempotency UNIQUE USING INDEX tr_idempotency_idx;
                """,
                    reverse_sql="""
                ALTER TABLE payment_transactionitem DROP CONSTRAINT IF EXISTS
                unique_transaction_idempotency;
                """,
                ),
                # Create back the index introduced in 0054, which was converted to
                # constraint
                migrations.RunSQL(
                    sql=migrations.RunSQL.noop,
                    reverse_sql="""
                    CREATE UNIQUE INDEX CONCURRENTLY "tr_idempotency_idx"
                    ON "payment_transactionitem" ("app_identifier", "idempotency_key");
                    """,
                ),
                migrations.RunSQL(
                    sql="""
                ALTER TABLE payment_transactionevent ADD CONSTRAINT
                unique_transaction_event_idempotency UNIQUE USING INDEX
                tr_event_idempotency_idx;
                """,
                    reverse_sql="""
                ALTER TABLE payment_transactionevent DROP CONSTRAINT  IF EXISTS
                unique_transaction_event_idempotency;
                """,
                ),
                # Create back the index introduced in 0054, which was converted to
                # constraint
                migrations.RunSQL(
                    sql=migrations.RunSQL.noop,
                    reverse_sql="""
                    CREATE UNIQUE INDEX CONCURRENTLY "tr_event_idempotency_idx"
                    ON "payment_transactionevent" ("transaction_id", "idempotency_key");
                    """,
                ),
            ],
            state_operations=[
                migrations.AddConstraint(
                    model_name="transactionevent",
                    constraint=models.UniqueConstraint(
                        fields=("transaction_id", "idempotency_key"),
                        name="unique_transaction_event_idempotency",
                    ),
                ),
                migrations.AddConstraint(
                    model_name="transactionitem",
                    constraint=models.UniqueConstraint(
                        fields=("app_identifier", "idempotency_key"),
                        name="unique_transaction_idempotency",
                    ),
                ),
            ],
        )
    ]
