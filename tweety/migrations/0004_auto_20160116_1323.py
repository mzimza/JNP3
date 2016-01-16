# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweety', '0003_tweet_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='origin',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='tweety.Tweet'),
        ),
    ]
