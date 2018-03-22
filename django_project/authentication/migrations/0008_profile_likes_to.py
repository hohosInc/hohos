# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20170304_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='likes_to',
            field=models.IntegerField(default=1),
        ),
    ]
