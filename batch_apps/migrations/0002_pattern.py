# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('pattern_string', models.CharField(max_length=500)),
                ('is_active', models.BooleanField(default=False)),
                ('app', models.ForeignKey(to='batch_apps.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
