# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0007_auto_20171105_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='chataccount',
            name='signed_in',
            field=models.BooleanField(default=False),
        ),
    ]
