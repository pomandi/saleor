# Generated by Django 2.2.9 on 2020-01-14 14:29

import uuid

import django.db.models.deletion
from django.db import migrations, models


def get_or_create_warehouse(apps):
    Warehouse = apps.get_model("warehouse", "Warehouse")
    ShippingZone = apps.get_model("shipping", "ShippingZone")
    Site = apps.get_model("sites", "Site")

    warehouses = Warehouse.objects.annotate(
        zones_count=models.Count("shipping_zones")
    ).filter(zones_count=ShippingZone.objects.count())
    if warehouses.first() is not None:
        return warehouses.first()

    site_settings = Site.objects.get_current().settings
    address = getattr(site_settings, "company_address", None)
    if address is None:
        Address = apps.get_model("account", "Address")
        address = Address.objects.create()

    warehouse = Warehouse.objects.create(name="Default warehouse", address=address)
    warehouse.shipping_zones.add(*ShippingZone.objects.all())
    return warehouse


def forward(apps, schema_editor):
    ProductVariant = apps.get_model("product", "ProductVariant")
    Stock = apps.get_model("warehouse", "Stock")

    if not ProductVariant.objects.exists():
        return

    product_variants = ProductVariant.objects.all()
    warehouse = get_or_create_warehouse(apps)
    stocks = [
        Stock(
            product_variant=variant,
            warehouse=warehouse,
            quantity=variant.quantity,
            quantity_allocated=variant.quantity_allocated,
        )
        for variant in product_variants.iterator()
    ]
    Stock.objects.bulk_create(stocks)


def backward(apps, schema_editor):
    ProductVariant = apps.get_model("product", "ProductVariant")
    Stock = apps.get_model("warehouse", "Stock")

    stocks = (
        Stock.objects.values("product_variant_id")
        .annotate(quantity_sum=models.Sum("quantity"))
        .annotate(quantity_allocated_sum=models.Sum("quantity_allocated"))
    )
    product_variants = ProductVariant.objects.all()
    for variant in product_variants.iterator():
        variant_dict = stocks.get(product_variant=variant)
        variant.quantity = variant_dict["quantity_sum"]
        variant.quantity_allocated = variant_dict["quantity_allocated_sum"]
        variant.save(update_fields=["quantity", "quantity_allocated"])

    Stock.objects.all().delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("account", "0037_auto_20191219_0944"),
        ("shipping", "0017_django_price_2"),
        ("product", "0110_auto_20191108_0340"),
        ("site", "0025_auto_20191024_0552"),
    ]

    operations = [
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Warehouse name"),
                ),
                (
                    "company_name",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Legal company name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        default="",
                        max_length=254,
                        verbose_name="Email address",
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="account.Address",
                    ),
                ),
                (
                    "shipping_zones",
                    models.ManyToManyField(blank=True, to="shipping.ShippingZone"),
                ),
            ],
            options={"ordering": ("-name",)},
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=0)),
                ("quantity_allocated", models.PositiveIntegerField(default=0)),
                (
                    "product_variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stock",
                        to="product.ProductVariant",
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="warehouse.Warehouse",
                    ),
                ),
            ],
            options={"unique_together": {("warehouse", "product_variant")}},
        ),
        migrations.RunPython(forward, backward),
    ]
