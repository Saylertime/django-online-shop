# Generated by Django 4.1.5 on 2023-01-25 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
