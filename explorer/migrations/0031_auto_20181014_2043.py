# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-14 20:43
from __future__ import unicode_literals

from django.db import migrations
from explorer.models import MessengerType, ChatType
from django.conf import settings


def create_vk_messenger_type(apps, schema_editor):
  messenger_type = MessengerType()
  messenger_type.id = 2
  messenger_type.name = "VK"
  messenger_type.save()

class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0030_auto_20180314_1823'),
    ]

    operations = [
        migrations.RunPython(create_vk_messenger_type),
    ]

