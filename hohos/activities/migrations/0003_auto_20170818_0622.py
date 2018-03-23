# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20170304_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(max_length=5, choices=[('L', 'Like'), ('LP', 'Like Profile'), ('WP', 'WP'), ('CHL', 'CHL'), ('RSPND', 'RSPND'), ('RESPDIND', 'RESPDIND')]),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=5, choices=[('L', 'Liked'), ('LP', 'Liked Profile'), ('C', 'Commented'), ('S', 'Also Commented'), ('WP', 'WP'), ('CHL', 'CHL'), ('RSPND', 'RSPND'), ('RESPDIND', 'RESPDIND')]),
        ),
    ]
