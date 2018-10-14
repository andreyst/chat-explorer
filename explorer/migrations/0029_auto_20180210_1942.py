# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-10 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0028_auto_20171115_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='continue_update_from',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chat',
            name='is_being_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chat',
            name='update_generation',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chat',
            name='update_started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]