# Generated by Django 3.0.6 on 2020-08-06 09:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0016_auto_20200423_0314"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="payment_method_type",
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
