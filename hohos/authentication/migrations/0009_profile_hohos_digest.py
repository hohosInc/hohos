# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_profile_likes_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='hohos_digest',
            field=models.BooleanField(default=True),
        ),
    ]
