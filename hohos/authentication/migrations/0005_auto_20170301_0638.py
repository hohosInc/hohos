# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-01 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20170301_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='job',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='what are you doing now?'),
        ),
    ]