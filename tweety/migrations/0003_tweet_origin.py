# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweety', '0002_auto_20160116_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='origin',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tweety.Tweet'),
        ),
    ]
