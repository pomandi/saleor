# Generated by Django 3.2.6 on 2021-08-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0146_auto_20210518_0945"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categorytranslation",
            name="language_code",
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name="collectiontranslation",
            name="language_code",
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name="producttranslation",
            name="language_code",
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name="productvarianttranslation",
            name="language_code",
            field=models.CharField(max_length=35),
        ),
    ]
