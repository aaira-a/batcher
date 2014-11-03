# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0010_execution_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='frequency',
            field=models.CharField(blank=True, default='', choices=[('daily', 'daily'), ('weekly - mondays', 'weekly - mondays'), ('weekly - tuesdays', 'weekly - tuesdays'), ('weekly - wednesdays', 'weekly - wednesdays'), ('weekly - thursdays', 'weekly - thursdays'), ('weekly - fridays', 'weekly - fridays'), ('weekly - saturdays', 'weekly - saturdays'), ('weekly - sundays', 'weekly - sundays'), ('monthly - 1st day', 'monthly - 1st day')], max_length=500),
        ),
    ]
