# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0011_chatchannel_remote_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatchannel',
            name='title',
            field=models.CharField(default='', max_length=4096),
        ),
    ]
