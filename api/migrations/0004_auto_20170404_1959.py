# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 16:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170329_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationresult',
            name='maze',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_results', to='api.Maze'),
        ),
        migrations.AlterField(
            model_name='evaluationresult',
            name='snippet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_results', to='api.Snippet'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL),
        ),
    ]
