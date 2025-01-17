# Generated by Django 4.2 on 2024-11-27 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('page_count', models.IntegerField(verbose_name='Количество страниц')),
                ('isbn', models.CharField(max_length=13, unique=True)),
            ],
        ),
    ]
