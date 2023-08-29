# Generated by Django 4.1.5 on 2023-01-21 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0014_category_has_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcat', to='app_goods.category', verbose_name='категория'),
        ),
    ]
