# Generated by Django 5.2 on 2025-04-10 14:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nation', '0021_nation_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nation',
            name='PKB',
            field=models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(1, message='PKB must be greater than 0')], verbose_name='PKB'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='banners/', verbose_name='Banner'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='coat_of_arms',
            field=models.ImageField(blank=True, null=True, upload_to='coats_of_arms/', verbose_name='Coat of Arms'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='flag',
            field=models.ImageField(blank=True, null=True, upload_to='flags/', verbose_name='Flag'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='population',
            field=models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(1, message='Population must be greater than 0')], verbose_name='Population'),
        ),
    ]
