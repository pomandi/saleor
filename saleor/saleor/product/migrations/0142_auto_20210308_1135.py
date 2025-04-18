# Generated by Django 3.1.7 on 2021-03-08 11:35

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0141_update_descritpion_fields"),
    ]

    operations = [
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="category",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="category_p_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="category",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="category_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="collection",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="collection_p_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="collection",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="collection_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="digitalcontent",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="digitalcontent_p_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="digitalcontent",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="digitalcontent_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="product",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="product_p_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="product",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="product_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="producttype",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="producttype_p_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="producttype",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="producttype_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="productvariant",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="productvariant_p_meta_idx"
            ),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="productvariant",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="productvariant_meta_idx"
            ),
        ),
    ]
