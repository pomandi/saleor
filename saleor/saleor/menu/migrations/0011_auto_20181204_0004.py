# Generated by Django 2.1.3 on 2018-12-04 06:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("menu", "0010_auto_20180913_0841")]

    operations = [
        migrations.AlterModelOptions(
            name="menu",
            options={
                "ordering": ["pk"],
                "permissions": (("manage_menus", "Manage navigation."),),
            },
        )
    ]
