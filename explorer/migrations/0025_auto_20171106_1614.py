# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 16:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('explorer', '0024_chatchannel_remote_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('remote_id', models.BigIntegerField(default=0)),
                ('remote_type', models.IntegerField(default=0)),
                ('title', models.CharField(default='', max_length=4096)),
                ('original_title', models.CharField(default='', max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('remote_id', models.BigIntegerField(default=0)),
                ('date', models.DateTimeField()),
                ('from_id', models.BigIntegerField(default=0)),
                ('author_name', models.CharField(default='', max_length=4096)),
                ('text', models.CharField(max_length=4096)),
            ],
        ),
        migrations.RenameModel(
            old_name='ChatAccount',
            new_name='Account',
        ),
        migrations.RenameModel(
            old_name='ChannelType',
            new_name='ChatType',
        ),
        migrations.RemoveField(
            model_name='chatchannel',
            name='chat_account',
        ),
        migrations.RemoveField(
            model_name='chatchannel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='chat_account',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='chat_channel',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='user',
        ),
        migrations.DeleteModel(
            name='ChatChannel',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
        migrations.AddField(
            model_name='message',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='explorer.Account'),
        ),
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='explorer.Chat'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='explorer.Account'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
