# Generated by Django 2.1.5 on 2019-02-06 15:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("payment", "0006_auto_20190109_0358")]

    operations = [
        migrations.AlterModelOptions(name="transaction", options={"ordering": ("pk",)})
    ]
