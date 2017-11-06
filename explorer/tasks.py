# Create your tasks here
from __future__ import absolute_import, unicode_literals
from __future__ import print_function
from celery import shared_task
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import Message as TlMessage
from time import sleep
import os
import pprint
import json
import sys
from django.conf import settings
from .models import Account, Chat, Message
from celery.utils.log import get_task_logger
from django.utils.timezone import make_aware

logger = get_task_logger(__name__)

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
@shared_task
def sync_telegram_chat(chat_id):
  try:
    chat = Chat.objects.get(id=chat_id)
  except Chat.DoesNotExist:
    logger.info("Channel %s does not exists" % chat_id)
    return False

  telethon_session = settings.TELETHON_SESSIONS_DIR + "/" + str(chat.account.login)
  client = TelegramClient(telethon_session, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  client.connect()  # Must return True, otherwise, try again

  if not client.is_user_authorized():
    logger.info("Chat account %s is not authorized" % chat.account.login)
    return False

  # chat
  if chat.remote_type == 1:
    peer = PeerUser(chat.remote_id)
  elif chat.remote_type == 2:
    peer = PeerChat(chat.remote_id)
  elif chat.remote_type == 3:
    peer = PeerChannel(chat.remote_id)
  else:
    raise ValueError("Unknown channel type " + chat.remote_type)

  chat_tl_entity = client.get_entity(peer)
  offset_id = 0
  author_ids = set()
  author_names = {}

  while True:
    (total_messages_count, messages_slice, senders) = client.get_message_history(chat_tl_entity, limit=3, offset_id=offset_id)
    if len(messages_slice) == 0:
      break

    offset_id = messages_slice[-1].id
    # eprint("%s, %s" % (messages_slice[-1].date, len(messages_slice)))

    messages = []

    for tl_message in messages_slice:
      if not isinstance(tl_message, TlMessage):
        logger.info("Skipping non-message %s" % pprint.pformat(tl_message))
        continue

      if tl_message.from_id not in author_ids:
        author = client.get_entity(PeerUser(tl_message.from_id))
        author_name = author.first_name
        if author.last_name is not None:
          author_name += " " + author.last_name
        author_names[tl_message.from_id] = author_name
        author_ids.add(tl_message.from_id)

      author_name = author_names[tl_message.from_id]
      message = Message()
      message.user = chat.user
      message.account = chat.account
      message.chat = chat
      message.remote_id = tl_message.id
      # TODO: make aware of correct timezone
      message.date = make_aware(tl_message.date)
      message.from_id = tl_message.from_id
      message.author_name = author_name
      message.text = tl_message.message
      messages.append(message)

    Message.objects.bulk_create(messages)
    logger.info("Saved %d messages" % len(messages))

  return True

@shared_task
def test(x, y):
    return x + y
