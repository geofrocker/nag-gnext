# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-20 12:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='nag_after',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='check',
            name='nag_interval',
            field=models.DurationField(default=datetime.timedelta(0, 60)),
        ),
        migrations.AddField(
            model_name='check',
            name='nag_status',
            field=models.BooleanField(default=True),
        ),
    ]
