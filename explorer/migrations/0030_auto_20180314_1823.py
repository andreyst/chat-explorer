# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-14 18:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0029_auto_20180210_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='login',
            new_name='name',
        ),
    ]
