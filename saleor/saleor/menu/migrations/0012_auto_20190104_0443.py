# Generated by Django 2.1.4 on 2019-01-04 10:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("menu", "0011_auto_20181204_0004")]

    operations = [
        migrations.AlterModelOptions(
            name="menu",
            options={
                "ordering": ("pk",),
                "permissions": (("manage_menus", "Manage navigation."),),
            },
        )
    ]
