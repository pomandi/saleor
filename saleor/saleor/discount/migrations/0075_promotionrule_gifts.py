# Generated by Django 3.2.23 on 2024-01-19 14:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0190_merge_20231221_1356"),
        ("discount", "0074_auto_20240119_1029"),
    ]

    operations = [
        migrations.AddField(
            model_name="promotionrule",
            name="gifts",
            field=models.ManyToManyField(
                blank=True,
                related_name="+",
                to="product.ProductVariant",
            ),
        ),
        migrations.AlterField(
            model_name="promotionrule",
            name="reward_type",
            field=models.CharField(
                blank=True,
                choices=[("subtotal_discount", "subtotal_discount"), ("gift", "gift")],
                max_length=255,
                null=True,
            ),
        ),
    ]
