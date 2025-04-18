# Generated by Django 3.2.6 on 2021-11-30 08:19

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0155_merge_20211208_1108"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="search_document",
            field=models.TextField(blank=True, default=""),
        ),
        # nosemgrep: add-index-concurrently
        migrations.AddIndex(
            model_name="product",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_document"],
                name="product_search_gin",
                opclasses=["gin_trgm_ops"],
            ),
        ),
        migrations.RemoveIndex(
            model_name="product",
            name="product_pro_search__e78047_gin",
        ),
        migrations.RemoveField(
            model_name="product",
            name="search_vector",
        ),
        migrations.RunSQL(
            """
            DROP TRIGGER IF EXISTS title_vector_update
            ON product_product
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            """
            DROP TRIGGER IF EXISTS tsvectorupdate
            ON product_product
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
