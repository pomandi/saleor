# Generated by Django 3.2.20 on 2023-08-18 08:35

import uuid

import django.db.models.deletion
from django.db import migrations, models

import saleor.core.utils.json_serializer


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0025_auto_20230420_1544"),
        ("account", "0082_user_last_confirm_email_request"),
        ("discount", "0048_old_sale_ids_sequence"),
    ]

    operations = [
        migrations.CreateModel(
            name="PromotionEvent",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("promotion_created", "Promotion created"),
                            ("promotion_updated", "Promotion updated"),
                            ("promotion_started", "Promotion started"),
                            ("promotion_ended", "Promotion ended"),
                            ("rule_created", "Rule created"),
                            ("rule_updated", "Rule updated"),
                            ("rule_deleted", "Rule deleted"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "parameters",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                    ),
                ),
                (
                    "app",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="promotion_events",
                        to="app.app",
                    ),
                ),
                (
                    "promotion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="discount.promotion",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="promotion_events",
                        to="account.user",
                    ),
                ),
            ],
            options={
                "ordering": ("date",),
            },
        ),
    ]
