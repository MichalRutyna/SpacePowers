# Generated by Django 4.2.17 on 2025-02-01 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nation', '0009_alter_unit_size_alter_unit_upkeep_per_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nation',
            name='PKB',
            field=models.PositiveIntegerField(default=0, verbose_name='PKB'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='population',
            field=models.PositiveIntegerField(default=0, verbose_name='Population'),
        ),
    ]
