# Generated by Django 3.1 on 2020-09-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plugins", "0005_auto_20200810_1415"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pluginconfiguration",
            name="active",
            field=models.BooleanField(default=False),
        ),
    ]
