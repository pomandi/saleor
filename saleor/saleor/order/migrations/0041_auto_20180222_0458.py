# Generated by Django 2.0.2 on 2018-02-22 10:58

from django.db import migrations


def assign_order_to_lines(apps, schema_editor):
    OrderLine = apps.get_model("order", "OrderLine")
    for line in OrderLine.objects.all():
        line.order = line.delivery_group.order
        line.save(update_fields=["order"])


def assign_delivery_group_to_lines(apps, schema_editor):
    Order = apps.get_model("order", "Order")
    OrderLine = apps.get_model("order", "OrderLine")
    for order in Order.objects.all():
        delivery_group = order.groups.create()
        for line in OrderLine.objects.filter(order=order):
            line.delivery_group = delivery_group
            line.save(update_fields=["delivery_group"])


class Migration(migrations.Migration):
    dependencies = [("order", "0040_auto_20180210_0422")]

    operations = [
        migrations.RunPython(assign_order_to_lines, assign_delivery_group_to_lines)
    ]
