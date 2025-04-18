# Generated by Django 2.0.3 on 2018-05-30 12:26
import uuid

from django.db import migrations, models


def get_token():
    return str(uuid.uuid4())


class Migration(migrations.Migration):
    dependencies = [("account", "0019_auto_20180528_1205")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="token",
            field=models.UUIDField(default=get_token, editable=False),
        )
    ]
