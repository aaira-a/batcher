# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0008_execution_due_executed'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='frequency',
            field=models.CharField(default='daily', max_length=500),
            preserve_default=True,
        ),
    ]
