# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-28 06:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usp', models.CharField(blank=True, max_length=80, null=True)),
                ('about', models.TextField(blank=True, max_length=255, null=True)),
                ('is_product', models.BooleanField(default=False)),
                ('company', models.CharField(blank=True, max_length=70, null=True)),
                ('facebook', models.CharField(blank=True, max_length=255, null=True)),
                ('quora', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter', models.CharField(blank=True, max_length=255, null=True)),
                ('likes', models.IntegerField(default=0)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('url', models.CharField(blank=True, max_length=50, null=True)),
                ('job_title', models.CharField(blank=True, max_length=50, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=7, null=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to='profile_pictures', width_field='width_field')),
                ('height_field', models.IntegerField(default=450)),
                ('width_field', models.IntegerField(default=350)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auth_profile',
            },
        ),
    ]
