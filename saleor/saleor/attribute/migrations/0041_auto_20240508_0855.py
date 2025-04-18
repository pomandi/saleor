# Generated by Django 3.2.22 on 2024-05-08 08:55

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ("attribute", "0040_auto_20240508_0854"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                    CREATE UNIQUE INDEX CONCURRENTLY temp_uniq_value_page
                    ON attribute_assignedpageattributevalue
                    ("value_id", "page_uniq");
                    """,
                    reverse_sql="""
                    DROP INDEX CONCURRENTLY IF EXISTS temp_uniq_value_page
                    """,
                ),
                migrations.RunSQL(
                    sql="""
                    ALTER TABLE attribute_assignedpageattributevalue
                    ADD CONSTRAINT temp_uniq_value_page
                    UNIQUE USING INDEX temp_uniq_value_page;
                    """,
                    reverse_sql="""
                    ALTER TABLE attribute_assignedpageattributevalue DROP CONSTRAINT
                    IF EXISTS temp_uniq_value_page;
                    """,
                ),
                migrations.RunSQL(
                    sql="""
                    CREATE UNIQUE INDEX CONCURRENTLY temp_uniq_value_product
                    ON attribute_assignedproductattributevalue
                    ("value_id", "product_uniq");
                    """,
                    reverse_sql="""
                    DROP INDEX CONCURRENTLY IF EXISTS temp_uniq_value_product
                    """,
                ),
                migrations.RunSQL(
                    sql="""
                    ALTER TABLE attribute_assignedproductattributevalue
                    ADD CONSTRAINT temp_uniq_value_product
                    UNIQUE USING INDEX temp_uniq_value_product;
                    """,
                    reverse_sql="""
                    ALTER TABLE attribute_assignedproductattributevalue DROP CONSTRAINT
                    IF EXISTS temp_uniq_value_product;
                    """,
                ),
            ]
        )
    ]
