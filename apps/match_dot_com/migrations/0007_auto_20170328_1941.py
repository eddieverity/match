# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match_dot_com', '0006_auto_20170328_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='user_pic',
            field=models.FileField(upload_to='match_dot_com/img'),
        ),
    ]
