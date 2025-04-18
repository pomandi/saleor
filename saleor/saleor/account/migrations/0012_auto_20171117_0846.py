# Generated by Django 1.11.5 on 2017-11-17 14:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("account", "0011_auto_20171110_0552")]

    replaces = [("userprofile", "0012_auto_20171117_0846")]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "permissions": (
                    ("view_user", "Can view users"),
                    ("edit_user", "Can edit users"),
                    ("view_group", "Can view groups"),
                    ("edit_group", "Can edit groups"),
                    ("view_staff", "Can view staff"),
                    ("edit_staff", "Can edit staff"),
                    ("impersonate_user", "Can impersonate users"),
                ),
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        )
    ]
