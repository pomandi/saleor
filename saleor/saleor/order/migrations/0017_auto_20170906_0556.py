# Generated by Django 1.11.4 on 2017-09-06 10:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("order", "0016_order_language_code")]

    operations = [
        migrations.AlterField(
            model_name="ordernote",
            name="content",
            field=models.CharField(max_length=250, verbose_name="content"),
        )
    ]
