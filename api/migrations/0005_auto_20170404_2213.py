# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 19:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170404_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
