# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0025_auto_20171106_1614'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['chat_id', 'date', 'remote_id'], name='explorer_me_chat_id_9353aa_idx'),
        ),
    ]