# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0003_auto_20171105_1815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chataccount',
            old_name='phone',
            new_name='login',
        ),
        migrations.AlterField(
            model_name='chataccount',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
