# Generated by Django 3.2.12 on 2022-02-25 12:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0132_rewrite_order_relations"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="token",
            new_name="id",
        ),
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ("-number",),
                "permissions": (("manage_orders", "Manage orders."),),
            },
        ),
    ]
