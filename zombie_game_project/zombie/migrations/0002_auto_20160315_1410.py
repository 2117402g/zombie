# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zombie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('desc', models.CharField(unique=True, max_length=256)),
                ('Btype', models.CharField(max_length=8)),
                ('criteria', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('icon', models.ImageField(upload_to=b'badge_icon', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='achievement',
            name='badge',
            field=models.ForeignKey(to='zombie.Badge'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='achievement',
            name='player',
            field=models.ForeignKey(to='zombie.UserProfile'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='current_game',
            field=models.CharField(max_length=1024, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='games_played',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='most_days_survived',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='most_kills',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='most_people',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
