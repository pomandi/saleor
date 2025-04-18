# Generated by Django 3.2.25 on 2024-04-05 07:56

from django.db import migrations
from django.db.models.expressions import Exists, OuterRef
from django.forms import model_to_dict

# The batch of size 250 takes ~0.5 second and consumes ~20MB memory at peak
ADDRESS_UPDATE_BATCH_SIZE = 250


def queryset_in_batches(queryset):
    """Slice a queryset into batches.

    Input queryset should be sorted be pk.
    """
    start_pk = 0

    while True:
        qs = queryset.filter(pk__gt=start_pk)[:ADDRESS_UPDATE_BATCH_SIZE]
        pks = list(qs.values_list("pk", flat=True))
        if not pks:
            break
        yield pks
        start_pk = pks[-1]


def update_checkout_addresses(apps, schema_editor):
    Checkout = apps.get_model("checkout", "Checkout")
    Warehouse = apps.get_model("warehouse", "Warehouse")
    Address = apps.get_model("account", "Address")

    queryset = Checkout.objects.filter(
        Exists(Warehouse.objects.filter(address_id=OuterRef("shipping_address_id"))),
    ).order_by("pk")

    for batch_pks in queryset_in_batches(queryset):
        checkouts = Checkout.objects.filter(pk__in=batch_pks)
        addresses = []
        for checkout in checkouts:
            if cc_address := checkout.shipping_address:
                checkout_address = Address(**model_to_dict(cc_address, exclude=["id"]))
                checkout.shipping_address = checkout_address
                addresses.append(checkout_address)
        Address.objects.bulk_create(addresses, ignore_conflicts=True)
        Checkout.objects.bulk_update(checkouts, ["shipping_address"])


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0066_merge_0063_auto_20240402_1114_0065_checkout_tax_error"),
    ]

    operations = [
        migrations.RunPython(update_checkout_addresses, migrations.RunPython.noop),
    ]
