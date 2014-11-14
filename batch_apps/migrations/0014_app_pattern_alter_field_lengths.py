# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_apps', '0013_app_country_category_repo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='category',
            field=models.CharField(blank=True, default='', choices=[('consumer', 'consumer'), ('customer', 'customer')], max_length=16),
        ),
        migrations.AlterField(
            model_name='app',
            name='country',
            field=models.CharField(blank=True, default='', choices=[('MY', 'MY'), ('SG', 'SG')], max_length=16),
        ),
        migrations.AlterField(
            model_name='app',
            name='frequency',
            field=models.CharField(blank=True, default='', choices=[('daily', 'daily'), ('weekly - mondays', 'weekly - mondays'), ('weekly - tuesdays', 'weekly - tuesdays'), ('weekly - wednesdays', 'weekly - wednesdays'), ('weekly - thursdays', 'weekly - thursdays'), ('weekly - fridays', 'weekly - fridays'), ('weekly - saturdays', 'weekly - saturdays'), ('weekly - sundays', 'weekly - sundays'), ('monthly - day 01', 'monthly - day 01')], max_length=64),
        ),
        migrations.AlterField(
            model_name='app',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='app',
            name='repo',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='pattern',
            name='name_pattern',
            field=models.CharField(max_length=128),
        ),
    ]
