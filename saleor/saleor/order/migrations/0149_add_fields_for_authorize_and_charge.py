# Generated by Django 3.2.13 on 2022-05-17 10:17

from django.db import migrations, models


def set_total_authorized_amount(apps, _schema_editor):
    Transaction = apps.get_model("payment", "Transaction")
    TransactionItem = apps.get_model("payment", "TransactionItem")
    Order = apps.get_model("order", "Order")

    # We don't store authorized amount directly in payment model. We need to find
    # all auth transactions, that are success and doesn't require any action, then
    # annotate the sum of them and assign to order as a `total_authorized_amount`.
    # The payment status `not-charged` exists only in case when payment is not paid yet.
    transaction_amounts = Transaction.objects.filter(
        payment__order_id=models.OuterRef("id"),
        payment__is_active=True,
        payment__charge_status="not-charged",
        is_success=True,
        action_required=False,
        kind="auth",
    ).values("payment__order_id")

    transactions_total_authorized_amounts = transaction_amounts.annotate(
        total_amount=models.Sum("amount", output_field=models.DecimalField())
    ).values("total_amount")

    Order.objects.filter(models.Exists(transactions_total_authorized_amounts)).update(
        total_authorized_amount=models.Subquery(transactions_total_authorized_amounts)
    )

    transaction_items = TransactionItem.objects.filter(
        order_id=models.OuterRef("id")
    ).values("order_id")
    transaction_items_total_authorized_amount = transaction_items.annotate(
        total_authorized=models.Sum(
            "authorized_value", output_field=models.DecimalField()
        )
    ).values("total_authorized")

    transaction_items_total_charged_amount = transaction_items.annotate(
        total_charged=models.Sum("charged_value", output_field=models.DecimalField())
    ).values("total_charged")
    order_ids = TransactionItem.objects.all().values_list("order_id", flat=True)

    Order.objects.filter(id__in=order_ids).update(
        total_authorized_amount=models.F("total_authorized_amount")
        + models.Subquery(transaction_items_total_authorized_amount),
        total_charged_amount=models.F("total_charged_amount")
        + models.Subquery(transaction_items_total_charged_amount),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0148_auto_20220519_1118"),
        ("payment", "0036_auto_20220518_0732"),
    ]

    operations = [
        migrations.RunPython(
            set_total_authorized_amount, reverse_code=migrations.RunPython.noop
        ),
    ]
