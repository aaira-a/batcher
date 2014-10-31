# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0007_day_date_field_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='execution',
            name='is_due_today',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='execution',
            name='is_executed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
