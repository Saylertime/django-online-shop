# Generated by Django 4.1.5 on 2023-01-30 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0011_order_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='card_number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='номер карты'),
        ),
    ]
