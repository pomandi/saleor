# Generated by Django 2.0.3 on 2018-08-03 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("site", "0016_auto_20180719_0520")]

    operations = [
        migrations.CreateModel(
            name="SiteSettingsTranslation",
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
                ("header_text", models.CharField(blank=True, max_length=200)),
                ("description", models.CharField(blank=True, max_length=500)),
                (
                    "site_settings",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="site.SiteSettings",
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="sitesettingstranslation",
            unique_together={("language_code", "site_settings")},
        ),
    ]
