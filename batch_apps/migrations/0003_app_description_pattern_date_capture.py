# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0002_pattern'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='description',
            field=models.TextField(default='', max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pattern',
            name='date_pattern',
            field=models.CharField(default='', max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pattern',
            name='is_capturing_date',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
