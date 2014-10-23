# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0004_day_execution'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pattern',
            old_name='pattern_string',
            new_name='name_pattern',
        ),
    ]
