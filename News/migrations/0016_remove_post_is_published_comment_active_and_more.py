# Generated by Django 4.2.17 on 2025-04-07 15:27

from django.conf import settings
from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('News', '0015_alter_roll_post_alter_roll_roll_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_published',
        ),
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='comment',
            name='edited',
            field=models.BooleanField(default=False, verbose_name='Is edited'),
        ),
        migrations.AddField(
            model_name='comment',
            name='edited_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Edited'),
        ),
        migrations.AddField(
            model_name='post',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='post',
            name='approved_by_admin',
            field=models.BooleanField(default=False, verbose_name='Approved by admin'),
        ),
        migrations.AddField(
            model_name='post',
            name='edited',
            field=models.BooleanField(default=False, verbose_name='Is edited'),
        ),
        migrations.AddField(
            model_name='post',
            name='edited_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Edited'),
        ),
        migrations.AddField(
            model_name='post',
            name='published_by_user',
            field=models.BooleanField(default=False, verbose_name='Published by user'),
        ),
        migrations.AddField(
            model_name='post',
            name='published_override',
            field=models.BooleanField(blank=True, null=True, verbose_name='Published override'),
        ),
        migrations.AddField(
            model_name='post',
            name='update_subscribe',
            field=models.ManyToManyField(blank=True, related_name='subscribed_post', to=settings.AUTH_USER_MODEL, verbose_name='Subscribed'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Is published'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='metagame',
            field=models.BooleanField(default=False, verbose_name='Metagame'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=martor.models.MartorField(blank=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Published'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
        migrations.CreateModel(
            name='Arc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Arc_url')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Users')),
            ],
            options={
                'verbose_name': 'Arc(s)',
                'verbose_name_plural': 'Arcs',
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='arcs',
            field=models.ManyToManyField(blank=True, related_name='posts', to='News.arc', verbose_name='Arcs'),
        ),
    ]
