# Generated by Django 4.1.5 on 2023-01-20 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0007_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.BigIntegerField(verbose_name='телефон'),
        ),
    ]