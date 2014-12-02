# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0014_app_pattern_alter_field_lengths'),
    ]

    operations = [
        migrations.AlterField(
            model_name='execution',
            name='email',
            field=models.ForeignKey(blank=True, to='django_mailbox.Message', null=True),
        ),
    ]
