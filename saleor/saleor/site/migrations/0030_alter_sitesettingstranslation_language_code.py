# Generated by Django 3.2.6 on 2021-08-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("site", "0029_auto_20210120_0934"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettingstranslation",
            name="language_code",
            field=models.CharField(max_length=35),
        ),
    ]
