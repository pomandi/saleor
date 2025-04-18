# Generated by Django 3.2.12 on 2022-04-19 09:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("page", "0025_rename_created_page_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="publication_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RenameField(
            model_name="page",
            old_name="publication_date",
            new_name="published_at",
        ),
    ]
