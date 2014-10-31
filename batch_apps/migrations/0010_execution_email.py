# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_mailbox', '0003_messages_matched_processed'),
        ('batch_apps', '0009_app_frequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='execution',
            name='email',
            field=models.ForeignKey(null=True, to='django_mailbox.Message'),
            preserve_default=True,
        ),
    ]
