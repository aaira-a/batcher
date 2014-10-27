# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_mailbox', '0002_messages_sent_time_to_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='matched_batch_apps',
            field=models.BooleanField(default=False, verbose_name='Matched by BA'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='processed_batch_apps',
            field=models.BooleanField(default=False, verbose_name='Processed by BA'),
            preserve_default=True,
        ),
    ]
