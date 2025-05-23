# Generated by Django 4.2.17 on 2025-03-24 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0012_post_secrecy_roll_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at'], 'verbose_name': 'Post(s)', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterField(
            model_name='post',
            name='secrecy_roll',
            field=models.IntegerField(blank=True, null=True, verbose_name='Secrecy roll'),
        ),
        migrations.AlterField(
            model_name='post',
            name='secrecy_roll_description',
            field=models.TextField(blank=True, null=True, verbose_name='Secrecy roll description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='secrecy_roll_override',
            field=models.BooleanField(blank=True, null=True, verbose_name='Secrecy roll override'),
        ),
        migrations.AlterField(
            model_name='post',
            name='success_roll',
            field=models.IntegerField(blank=True, null=True, verbose_name='Success roll'),
        ),
        migrations.AlterField(
            model_name='post',
            name='success_roll_description',
            field=models.TextField(blank=True, null=True, verbose_name='Success roll description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='success_roll_override',
            field=models.BooleanField(blank=True, null=True, verbose_name='Success roll override'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='News.tag', verbose_name='Tags'),
        ),
    ]
