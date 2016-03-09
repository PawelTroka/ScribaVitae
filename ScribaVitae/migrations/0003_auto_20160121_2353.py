# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 22:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ScribaVitae', '0002_auto_20160121_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dateAdded',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 21, 22, 53, 4, 529028, tzinfo=utc), verbose_name='date published'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='literarywork',
            name='dateAdded',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 21, 22, 53, 9, 295544, tzinfo=utc), verbose_name='date published'),
            preserve_default=False,
        ),
    ]
