# Generated by Django 3.1.5 on 2021-02-12 09:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0139_description_vector_search"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="description_json",
        ),
        migrations.RemoveField(
            model_name="categorytranslation",
            name="description_json",
        ),
        migrations.RemoveField(
            model_name="collection",
            name="description_json",
        ),
        migrations.RemoveField(
            model_name="collectiontranslation",
            name="description_json",
        ),
        migrations.RemoveField(
            model_name="product",
            name="description_json",
        ),
        migrations.RemoveField(
            model_name="producttranslation",
            name="description_json",
        ),
    ]
