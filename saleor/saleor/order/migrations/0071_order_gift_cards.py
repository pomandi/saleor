# Generated by Django 2.2.1 on 2019-06-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("giftcard", "0001_initial"),
        ("order", "0070_drop_update_event_and_rename_events"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="gift_cards",
            field=models.ManyToManyField(
                blank=True, related_name="orders", to="giftcard.GiftCard"
            ),
        )
    ]
