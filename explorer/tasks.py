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
from django.db.models import Max
from celery.utils.log import get_task_logger
from django.utils.timezone import make_aware
from datetime import timedelta

logger = get_task_logger(__name__)

# In UTC
morning_starts_at = 3 # 6 MSK
day_starts_at = 9 # 12 MSK
evening_starts_at = 18 # 21 MSK
night_starts_at = 20 # 23 MSK

time_shift = morning_starts_at

morning_starts_at -= time_shift
day_starts_at     -= time_shift
evening_starts_at -= time_shift
night_starts_at   -= time_shift

if morning_starts_at <= 0: morning_starts_at += 24
if day_starts_at     <= 0: day_starts_at += 24
if evening_starts_at <= 0: evening_starts_at += 24
if night_starts_at   <= 0: night_starts_at += 24

# TODO: Make this transactional
@shared_task
def sync_telegram_chat(chat_id, offset_id=0):
  try:
    chat = Chat.objects.get(id=chat_id)
  except Chat.DoesNotExist:
    logger.info("Channel %s does not exists" % chat_id)
    return False

  telethon_session = settings.TELETHON_SESSIONS_DIR + "/" + str(chat.account.user_id) + "_" + str(chat.account.login)
  logger.info("Telethon session: %s" % telethon_session)

  client = TelegramClient(telethon_session, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  rc = client.connect()  # Must return True, otherwise, try again
  if not rc:
    logger.error("Chat account %s is not connected" % chat.account.login)
    return False

  if not client.is_user_authorized():
    logger.error("Chat account %s is not authorized" % chat.account.login)
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
  author_ids = set()
  author_names = {}

  if offset_id > 0:
    max_remote_id = Message.objects.filter(chat_id=chat.id, remote_id__lt=offset_id).aggregate(Max('remote_id'))
  else:
    max_remote_id = Message.objects.filter(chat_id=chat.id).aggregate(Max('remote_id'))
  max_remote_id = max_remote_id['remote_id__max']
  logger.info("Max remote id: %s" % max_remote_id)

  slice_len = 0
  (total_messages_count, messages_slice, senders) = client.get_message_history(chat_tl_entity, limit=100, offset_id=offset_id)

  if len(messages_slice) > 0:
    offset_id = messages_slice[-1].id
  # eprint("%s, %s" % (messages_slice[-1].date, len(messages_slice)))

  messages = []

  for tl_message in messages_slice:
    if tl_message.id == max_remote_id:
      logger.info("Downloaded message with max remote id: %s" % max_remote_id)
      break

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
    date = make_aware(tl_message.date)
    message.date = date
    daytime = calc_daytime(date)
    message.daytime = daytime
    message.from_id = tl_message.from_id
    message.author_name = author_name
    message.text = tl_message.message
    messages.append(message)

  Message.objects.bulk_create(messages)
  logger.info("Saved %d messages" % len(messages))

  if len(messages) > 0:
    logger.info("Sending next batch from offset_id=%s" % offset_id)
    sync_telegram_chat.delay(chat.id, offset_id)

  return True

def calc_daytime(date):
  date -= timedelta(hours=time_shift)
  daytime = Message.DAYTIME_MORNING
  if date.hour >= night_starts_at:
    daytime = Message.DAYTIME_NIGHT
  elif date.hour >= evening_starts_at:
    daytime = Message.DAYTIME_EVENING
  elif date.hour >= day_starts_at:
    daytime = Message.DAYTIME_DAY

  return daytime

@shared_task
def test(x, y):
    return x + y
