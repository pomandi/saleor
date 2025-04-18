# Generated by Django 3.2.6 on 2021-12-27 09:47

from django.apps import apps as registry
from django.db import migrations
from django.db.models.signals import post_migrate

from ...core.search_tasks import set_user_search_document_values


def update_user_search_document_values(apps, _schema_editor):
    def on_migrations_complete(sender=None, **kwargs):
        set_user_search_document_values.delay()

    sender = registry.get_app_config("account")
    post_migrate.connect(on_migrations_complete, weak=False, sender=sender)


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0057_user_search_document"),
    ]

    operations = [
        migrations.RunPython(
            update_user_search_document_values, reverse_code=migrations.RunPython.noop
        ),
    ]
