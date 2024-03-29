# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 12:11
from __future__ import unicode_literals

from django.db import migrations
from explorer.models import MessengerType, ChatType
from django.conf import settings

def create_types(apps, schema_editor):
  messenger_type = MessengerType()
  messenger_type.id = 1
  messenger_type.name = "Telegram"
  messenger_type.save()

  channel_type = ChatType()
  channel_type.id = 1
  channel_type.name = "User"
  channel_type.save()

  channel_type = ChatType()
  channel_type.id = 2
  channel_type.name = "Chat"
  channel_type.save()

  channel_type = ChatType()
  channel_type.id = 3
  channel_type.name = "Channel"
  channel_type.save()

class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0035_auto_20210119_1757'),
    ]

    operations = [
        migrations.RunPython(create_types),
    ]
