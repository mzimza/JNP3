# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 16:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweety', '0007_auto_20160116_1642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetyuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='tweetyuser',
            name='is_staff',
        ),
    ]
