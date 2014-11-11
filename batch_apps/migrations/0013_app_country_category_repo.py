# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0012_app_frequency_choices_datenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='category',
            field=models.CharField(default='', blank=True, choices=[('consumer', 'consumer'), ('customer', 'customer')], max_length=500),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='country',
            field=models.CharField(default='', blank=True, choices=[('MY', 'MY'), ('SG', 'SG')], max_length=500),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='repo',
            field=models.CharField(default='', blank=True, max_length=500),
            preserve_default=True,
        ),
    ]
