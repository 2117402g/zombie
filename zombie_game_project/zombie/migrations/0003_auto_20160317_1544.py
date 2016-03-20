# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zombie', '0002_auto_20160315_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'data/profile.png', upload_to=b'profile_images'),
        ),
    ]
