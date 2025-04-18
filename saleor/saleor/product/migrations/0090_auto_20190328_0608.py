# Generated by Django 2.1.7 on 2019-03-28 11:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("product", "0089_auto_20190225_0252")]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="tax_rate",
            field=models.CharField(
                blank=True,
                choices=[
                    ("accommodation", "accommodation"),
                    ("admission to cultural events", "admission to cultural events"),
                    (
                        "admission to entertainment events",
                        "admission to entertainment events",
                    ),
                    ("admission to sporting events", "admission to sporting events"),
                    ("advertising", "advertising"),
                    ("agricultural supplies", "agricultural supplies"),
                    ("baby foodstuffs", "baby foodstuffs"),
                    ("bikes", "bikes"),
                    ("books", "books"),
                    ("childrens clothing", "childrens clothing"),
                    ("domestic fuel", "domestic fuel"),
                    ("domestic services", "domestic services"),
                    ("e-books", "e-books"),
                    ("foodstuffs", "foodstuffs"),
                    ("hotels", "hotels"),
                    ("medical", "medical"),
                    ("newspapers", "newspapers"),
                    ("passenger transport", "passenger transport"),
                    ("pharmaceuticals", "pharmaceuticals"),
                    ("property renovations", "property renovations"),
                    ("restaurants", "restaurants"),
                    ("social housing", "social housing"),
                    ("standard", "standard"),
                    ("water", "water"),
                    ("wine", "wine"),
                ],
                max_length=128,
            ),
        ),
        migrations.AlterField(
            model_name="producttype",
            name="tax_rate",
            field=models.CharField(
                choices=[
                    ("accommodation", "accommodation"),
                    ("admission to cultural events", "admission to cultural events"),
                    (
                        "admission to entertainment events",
                        "admission to entertainment events",
                    ),
                    ("admission to sporting events", "admission to sporting events"),
                    ("advertising", "advertising"),
                    ("agricultural supplies", "agricultural supplies"),
                    ("baby foodstuffs", "baby foodstuffs"),
                    ("bikes", "bikes"),
                    ("books", "books"),
                    ("childrens clothing", "childrens clothing"),
                    ("domestic fuel", "domestic fuel"),
                    ("domestic services", "domestic services"),
                    ("e-books", "e-books"),
                    ("foodstuffs", "foodstuffs"),
                    ("hotels", "hotels"),
                    ("medical", "medical"),
                    ("newspapers", "newspapers"),
                    ("passenger transport", "passenger transport"),
                    ("pharmaceuticals", "pharmaceuticals"),
                    ("property renovations", "property renovations"),
                    ("restaurants", "restaurants"),
                    ("social housing", "social housing"),
                    ("standard", "standard"),
                    ("water", "water"),
                    ("wine", "wine"),
                ],
                max_length=128,
            ),
        ),
    ]
