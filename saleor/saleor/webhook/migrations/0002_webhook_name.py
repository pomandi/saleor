# Generated by Django 2.2.4 on 2019-10-02 06:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("webhook", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="webhook",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        )
    ]
