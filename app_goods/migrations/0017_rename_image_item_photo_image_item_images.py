# Generated by Django 4.1.5 on 2023-01-22 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0016_alter_review_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='image',
            new_name='photo',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_goods.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='fotki', to='app_goods.image'),
        ),
    ]