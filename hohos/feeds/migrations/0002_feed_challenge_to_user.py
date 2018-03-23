# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='challenge_to_user',
            field=models.ForeignKey(related_name='challenge_to_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
