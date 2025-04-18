# Generated by Django 3.1 on 2020-09-02 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0088_auto_20200812_1101"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="discount_amount",
            field=models.DecimalField(decimal_places=3, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name="order",
            name="shipping_price_gross_amount",
            field=models.DecimalField(
                decimal_places=3, default=0, editable=False, max_digits=12
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="shipping_price_net_amount",
            field=models.DecimalField(
                decimal_places=3, default=0, editable=False, max_digits=12
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_gross_amount",
            field=models.DecimalField(decimal_places=3, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_net_amount",
            field=models.DecimalField(decimal_places=3, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="unit_price_gross_amount",
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="unit_price_net_amount",
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
    ]
