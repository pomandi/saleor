# Generated by Django 3.2.20 on 2023-09-06 12:02

# Create tables that were used by package that is no longer used:
# - `django-prices-vatlayer` - removed in https://github.com/saleor/saleor/pull/13179/

# Creation of the tables is needed for schema consistency for replication.
# Normally we would be removing those tables, but cause of zero-downtime policy
# they cannot be removed from database until 3.16 version.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_drop_openexchangerates_table"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS django_prices_vatlayer_ratetypes(
                "id" serial4 NOT NULL PRIMARY KEY,
                "types" text NOT NULL
            );
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS django_prices_vatlayer_vat(
                "id" serial4 NOT NULL PRIMARY KEY,
                "country_code" varchar(2) NOT NULL,
                "data" text NOT NULL
            );
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
