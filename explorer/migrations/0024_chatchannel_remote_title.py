# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0023_auto_20171106_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatchannel',
            name='remote_title',
            field=models.CharField(default='', max_length=4096),
        ),
    ]