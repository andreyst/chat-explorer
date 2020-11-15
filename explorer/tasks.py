from __future__ import absolute_import, unicode_literals
from __future__ import print_function
from .models import Account, Chat, Message
from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import timedelta
from django.conf import settings
from django.db.models import Max
from django.db import transaction
from telethon.sync import TelegramClient
from telethon.tl.types import MessageService as TlMessageService
import asyncio

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
def sync_telegram_chat(chat_id, update_generation):
  logger.info("Starting update iteration of chat %s with update generation %s" % (chat_id, update_generation))

  try:
    chat = Chat.objects.get(id=chat_id, update_generation=update_generation)
  except Chat.DoesNotExist:
    logger.info("Channel {chat_id} with update generation {update_generation} does not exists" % chat_id)
    return False

  telethon_session = settings.TELETHON_SESSIONS_DIR + "/" + str(chat.account.user_id) + "_" + str(chat.account.name)
  logger.debug("Telethon session: %s" % telethon_session)

  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  client = TelegramClient(telethon_session, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  client.connect()
  if not client.is_user_authorized():
    logger.error("Chat account %s is not authorized" % chat.account.login)
    return False

  with client.start():
    chat_entity = client.get_entity(chat.remote_id)

    continue_update_from = chat.continue_update_from
    if continue_update_from == 0:
      max_remote_id = Message.objects.filter(chat_id=chat.id).aggregate(Max('remote_id'))
      max_remote_id = max_remote_id['remote_id__max']
      if max_remote_id is None:
        max_remote_id = 0
      continue_update_from = max_remote_id
    logger.info(f"Max remote id: {continue_update_from}")

    author_names = {}
    messages = []
    max_id = None

    # for message in client.iter_messages(chat_entity, reverse=True, limit=20, min_id=max_remote_id):
    for tl_message in client.iter_messages(chat_entity, reverse=True, limit=1000, min_id=continue_update_from):
        max_id = tl_message.id
        if isinstance(tl_message, TlMessageService):
          continue

        if tl_message.from_id.user_id not in author_names:
          author = client.get_entity(tl_message.from_id)
          author_name = author.first_name if author.first_name is not None else ""
          if author.last_name is not None:
            author_name += " " + author.last_name
          author_names[tl_message.from_id.user_id] = author_name

        author_name = author_names[tl_message.from_id.user_id]
        message = Message()
        message.user = chat.user
        message.account = chat.account
        message.chat = chat
        message.remote_id = tl_message.id
        message.date = tl_message.date
        daytime = calc_daytime(tl_message.date)
        message.daytime = daytime
        message.from_id = tl_message.from_id.user_id
        message.author_name = author_name
        message.text = tl_message.message
        messages.append(message)

    if max_id is not None:
      logger.info(f"Last message: {tl_message}")
      logger.info("Prepared %d messages to save" % (len(messages)))

      with transaction.atomic():
        sid = transaction.savepoint()

        if len(messages) > 0:
          Message.objects.bulk_create(messages)

        affected_rows = Chat.objects.filter(id=chat.id, update_generation=update_generation).update(
          continue_update_from=max_id
        )

        if affected_rows != 1:
          transaction.savepoint_rollback(sid)
          logger.warn("Failed to save %d messages because chat have changed its update generation from %s" % (len(messages), update_generation))
          return False

        transaction.savepoint_commit(sid)
        logger.info("Saved %d messages" % (len(messages)))
        logger.info(f"Scheduling next batch retrieval from id={max_id}")
        sync_telegram_chat.delay(chat.id, chat.update_generation)
    else:
      logger.info("Update fully completed")
      chat.is_being_updated = False
      chat.continue_update_from = 0
      chat.save()

    logger.info(f"Finished update iteration of chat {chat.id} with update generation {chat.update_generation}")

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
