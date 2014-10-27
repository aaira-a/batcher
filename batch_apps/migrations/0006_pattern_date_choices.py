# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0005_app_rename_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='date_pattern',
            field=models.CharField(choices=[('', ''), ('dd/mm/yyyy', 'dd/mm/yyyy'), ('mm/dd/yyyy', 'mm/dd/yyyy'), ('ddmm/yyyy', 'ddmm/yyyy'), ('mmdd/yyyy', 'mmdd/yyyy')], default='', max_length=64, blank=True),
        ),
    ]
