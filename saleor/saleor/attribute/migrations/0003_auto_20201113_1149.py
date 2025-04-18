# Generated by Django 3.1 on 2020-11-13 11:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attribute", "0002_auto_20201030_1141"),
    ]

    operations = [
        migrations.AddField(
            model_name="attributevalue",
            name="content_type",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="attributevalue",
            name="file_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="attribute",
            name="input_type",
            field=models.CharField(
                choices=[
                    ("dropdown", "Dropdown"),
                    ("multiselect", "Multi Select"),
                    ("file", "File"),
                ],
                default="dropdown",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="attribute",
            name="available_in_grid",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="attribute",
            name="filterable_in_dashboard",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="attribute",
            name="filterable_in_storefront",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
