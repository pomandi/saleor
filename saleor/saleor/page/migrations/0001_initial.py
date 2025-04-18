# Generated by Django 2.0.2 on 2018-03-02 01:50

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Page",
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
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("is_visible", models.BooleanField(default=False)),
                ("available_on", models.DateField(blank=True, null=True)),
            ],
            options={
                "ordering": ("slug",),
                "permissions": (
                    ("view_page", "Can view pages"),
                    ("edit_page", "Can edit pages"),
                ),
            },
        )
    ]
