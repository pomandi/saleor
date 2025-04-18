# Generated by Django 2.0.3 on 2018-08-03 10:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("product", "0065_auto_20180719_0520")]

    operations = [
        migrations.CreateModel(
            name="AttributeChoiceValueTranslation",
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
                ("language_code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=100)),
                (
                    "attribute_choice_value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="product.AttributeChoiceValue",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CategoryTranslation",
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
                (
                    "seo_title",
                    models.CharField(
                        blank=True,
                        max_length=70,
                        null=True,
                        validators=[django.core.validators.MaxLengthValidator(70)],
                    ),
                ),
                (
                    "seo_description",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        validators=[django.core.validators.MaxLengthValidator(300)],
                    ),
                ),
                ("language_code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField(blank=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="product.Category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CollectionTranslation",
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
                (
                    "seo_title",
                    models.CharField(
                        blank=True,
                        max_length=70,
                        null=True,
                        validators=[django.core.validators.MaxLengthValidator(70)],
                    ),
                ),
                (
                    "seo_description",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        validators=[django.core.validators.MaxLengthValidator(300)],
                    ),
                ),
                ("language_code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=128)),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="product.Collection",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductAttributeTranslation",
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
                ("language_code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=100)),
                (
                    "product_attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="product.ProductAttribute",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductTranslation",
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
                (
                    "seo_title",
                    models.CharField(
                        blank=True,
                        max_length=70,
                        null=True,
                        validators=[django.core.validators.MaxLengthValidator(70)],
                    ),
                ),
                (
                    "seo_description",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        validators=[django.core.validators.MaxLengthValidator(300)],
                    ),
                ),
                ("language_code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="product.Product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductVariantTranslation",
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
                ("language_code", models.CharField(max_length=10)),
                ("name", models.CharField(blank=True, max_length=255)),
                (
                    "product_variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="product.ProductVariant",
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="productvarianttranslation",
            unique_together={("language_code", "product_variant")},
        ),
        migrations.AlterUniqueTogether(
            name="producttranslation", unique_together={("language_code", "product")}
        ),
        migrations.AlterUniqueTogether(
            name="productattributetranslation",
            unique_together={("language_code", "product_attribute")},
        ),
        migrations.AlterUniqueTogether(
            name="collectiontranslation",
            unique_together={("language_code", "collection")},
        ),
        migrations.AlterUniqueTogether(
            name="categorytranslation", unique_together={("language_code", "category")}
        ),
        migrations.AlterUniqueTogether(
            name="attributechoicevaluetranslation",
            unique_together={("language_code", "attribute_choice_value")},
        ),
    ]
