# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match_dot_com', '0013_auto_20170329_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]