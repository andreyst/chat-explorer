# Create your tasks here
from __future__ import absolute_import, unicode_literals
from __future__ import print_function
from celery import shared_task
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import Message
from time import sleep
import os
import pprint
import json
import sys
from django.conf import settings
from .models import ChatAccount, ChatChannel, ChatMessage
from celery.utils.log import get_task_logger
from django.utils.timezone import make_aware

logger = get_task_logger(__name__)

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
@shared_task
def sync_telegram_channel(chat_channel_id):
  try:
    chat_channel = ChatChannel.objects.get(id=chat_channel_id)
  except ChatChannel.DoesNotExist:
    logger.info("Channel %s does not exists" % chat_channel_id)
    return False

  telethon_session = settings.TELETHON_SESSIONS_DIR + "/" + str(chat_channel.chat_account.login)
  client = TelegramClient(telethon_session, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  client.connect()  # Must return True, otherwise, try again

  if not client.is_user_authorized():
    logger.info("Chat account %s is not authorized" % chat_channel.chat_account.login)
    return False

  # chat
  if chat_channel.ttype == 1:
    peer = PeerUser(chat_channel.remote_id)
  elif chat_channel.ttype == 2:
    peer = PeerChat(chat_channel.remote_id)
  elif chat_channel.ttype == 3:
    peer = PeerChannel(chat_channel.remote_id)
  else:
    raise ValueError("Unknown channel type " + chat_channel.ttype)

  chat_tl_entity = client.get_entity(peer)
  offset_id = 0
  author_ids = set()
  author_names = {}

  while True:
    (total_messages_count, messages_slice, senders) = client.get_message_history(chat_tl_entity, limit=100, offset_id=offset_id)
    if len(messages_slice) == 0:
      break

    offset_id = messages_slice[-1].id
    # eprint("%s, %s" % (messages_slice[-1].date, len(messages_slice)))

    chat_message_models = []

    for message in messages_slice:
      if not isinstance(message, Message):
        logger.info("Skipping non-message %s" % pprint.pformat(message))
        continue

      if message.from_id not in author_ids:
        author = client.get_entity(PeerUser(message.from_id))
        author_name = author.first_name
        if author.last_name is not None:
          author_name += " " + author.last_name
        author_names[message.from_id] = author_name
        author_ids.add(message.from_id)

      author_name = author_names[message.from_id]
      chat_message_model = ChatMessage()
      chat_message_model.user = chat_channel.user
      chat_message_model.chat_account = chat_channel.chat_account
      chat_message_model.chat_channel = chat_channel
      chat_message_model.remote_id = message.id
      # TODO: make aware of correct timezone
      chat_message_model.date = make_aware(message.date)
      chat_message_model.from_id = message.from_id
      chat_message_model.author_name = author_name
      chat_message_model.text = message.message
      chat_message_models.append(chat_message_model)

    ChatMessage.objects.bulk_create(chat_message_models)
    logger.info("Saved %d messages " % len(chat_message_models))

  return True

@shared_task
def test(x, y):
    return x + y
