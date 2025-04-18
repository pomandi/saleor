# Generated by Django 1.11.4 on 2017-09-19 13:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("order", "0017_auto_20170906_0556")]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ("-last_status_change",),
                "permissions": (
                    ("view_order", "Can view orders"),
                    ("edit_order", "Can edit orders"),
                ),
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        )
    ]
