# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0010_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatchannel',
            name='remote_id',
            field=models.BigIntegerField(default=0),
        ),
    ]