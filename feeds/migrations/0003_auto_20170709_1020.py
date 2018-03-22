# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_feed_challenge_to_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='challenge_to_user',
            field=models.ForeignKey(related_name='challenge_to_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='to_user',
            field=models.ForeignKey(related_name='for_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
