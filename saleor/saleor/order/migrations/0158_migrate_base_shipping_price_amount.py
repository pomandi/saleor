# Generated by Django 4.0.7 on 2022-09-26 10:15

from django.db import migrations
from django.db.models import Case, When

AVATAX_PLUGIN_ID = "mirumee.taxes.avalara"


def set_base_shipping_price(apps, _schema_editor):
    Order = apps.get_model("order", "Order")
    PluginConfiguration = apps.get_model("plugins", "PluginConfiguration")
    SiteSettings = apps.get_model("site", "SiteSettings")
    Channel = apps.get_model("channel", "Channel")

    channel_ids_with_tax_included = set()
    channel_ids_with_tax_excluded = set()

    # Fetch channel ids with overrode `SiteSettings.include_taxes_in_prices`
    avatax_configs = PluginConfiguration.objects.filter(
        identifier=AVATAX_PLUGIN_ID, active=True
    )
    for config in avatax_configs:
        config_dict = {item["name"]: item["value"] for item in config.configuration}
        override_global_tax = config_dict.get("override_global_tax")
        if override_global_tax:
            include_taxes_in_prices = config_dict.get("include_taxes_in_prices")
            if include_taxes_in_prices:
                channel_ids_with_tax_included.add(config.channel_id)
            else:
                channel_ids_with_tax_excluded.add(config.channel_id)

    # Fetch channel ids with default settings
    channel_ids_with_override_config = channel_ids_with_tax_included.union(
        channel_ids_with_tax_excluded
    )
    site_settings = SiteSettings.objects.first()
    channel_ids_without_override_config = Channel.objects.exclude(
        id__in=channel_ids_with_override_config
    ).values_list("id", flat=True)
    if site_settings and site_settings.include_taxes_in_prices:
        channel_ids_with_tax_included.update(channel_ids_without_override_config)
    else:
        channel_ids_with_tax_excluded.update(channel_ids_without_override_config)

    # Set base shipping price for channels with tax included in prices
    Order.objects.filter(
        channel_id__in=channel_ids_with_tax_included.union(
            channel_ids_with_tax_excluded
        )
    ).update(
        base_shipping_price_amount=Case(
            When(
                channel_id__in=channel_ids_with_tax_included,
                then="shipping_price_gross_amount",
            ),
            When(
                channel_id__in=channel_ids_with_tax_excluded,
                then="shipping_price_net_amount",
            ),
            default="base_shipping_price_amount",
        )
    )


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0157_order_base_shipping_price_amount"),
        ("site", "0034_sitesettings_limit_quantity_per_checkout"),
        ("channel", "0005_channel_allocation_strategy"),
        ("plugins", "0010_auto_20220104_1239"),
    ]
    operations = [
        migrations.RunPython(
            set_base_shipping_price, reverse_code=migrations.RunPython.noop
        ),
    ]
