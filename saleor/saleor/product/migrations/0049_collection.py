# Generated by Django 1.11.5 on 2018-01-24 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("product", "0048_product_class_to_type")]

    operations = [
        migrations.CreateModel(
            name="CollectionProduct",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
            options={"db_table": "product_collection_products"},
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128, unique=True)),
                ("slug", models.SlugField()),
                (
                    "products",
                    models.ManyToManyField(
                        blank=True,
                        related_name="collections",
                        through="product.CollectionProduct",
                        to="product.Product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="collectionproduct",
            name="collection",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to="product.Collection"
            ),
        ),
        migrations.AddField(
            model_name="collectionproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to="product.Product"
            ),
        ),
    ]
