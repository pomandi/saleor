# Generated by Django 3.2.12 on 2022-02-24 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0131_change_pk_to_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fulfillment",
            name="order_token",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="order.order",
            ),
        ),
        migrations.AlterField(
            model_name="orderevent",
            name="order_token",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="order.order"
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="order_token",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="order.order",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="original_token",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="originals",
                to="order.order",
            ),
        ),
        migrations.RemoveField(
            model_name="fulfillment",
            name="order",
        ),
        migrations.RemoveField(
            model_name="orderevent",
            name="order",
        ),
        migrations.RemoveField(
            model_name="orderline",
            name="order",
        ),
        migrations.RemoveField(
            model_name="order",
            name="original",
        ),
        migrations.RenameField(
            model_name="fulfillment",
            old_name="order_token",
            new_name="order",
        ),
        migrations.RenameField(
            model_name="orderevent",
            old_name="order_token",
            new_name="order",
        ),
        migrations.RenameField(
            model_name="orderline",
            old_name="order_token",
            new_name="order",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="original_token",
            new_name="original",
        ),
        migrations.AlterField(
            model_name="fulfillment",
            name="order",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fulfillments",
                to="order.order",
            ),
        ),
        migrations.AlterField(
            model_name="orderevent",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="order.order",
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="order",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lines",
                to="order.order",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="original",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="order.order",
            ),
        ),
    ]
