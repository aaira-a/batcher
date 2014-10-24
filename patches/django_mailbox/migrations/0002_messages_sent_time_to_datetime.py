# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_mailbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_time',
            field=models.DateTimeField(verbose_name='Sent Time'),
        ),
    ]
