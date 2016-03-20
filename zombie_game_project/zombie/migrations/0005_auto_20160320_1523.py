# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zombie', '0004_auto_20160320_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
    ]
