from .models import MessengerType, Account, ChatType, Chat, Message
from .tasks import sync_telegram_chat
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.types import User as TelegramUser
import json
import pprint
import re
import asyncio

def login(request):
  user = authenticate(request, username=settings.DEFAULT_USER_NAME, password=settings.DEFAULT_USER_PASSWORD)
  if user is not None:
      django_login(request, user)
      return redirect("explorer:index")

  return HttpResponse("ERROR: Cannot authenticate default user")

def logout(request):
  django_logout(request)
  return redirect("explorer:index")

@login_required
def index(request):
  chats = Chat.objects.filter(user=request.user).all()
  # return HttpResponse(pprint.pformat(accounts))
  context = {
    'chats': chats,
  }
  return render(request, 'explorer/list_chats.html', context)

@login_required
def list_accounts(request):
  accounts = Account.objects.filter(user=request.user).all()
  context = {
    'accounts': accounts,
    'from' : request.GET.get('from', '')
  }
  return render(request, 'explorer/list_accounts.html', context)

@login_required
def add_account(request):
  if request.POST.get('submit') is None:
    return render(request, 'explorer/add_account.html', {})

  try:
    messenger_type = get_object_or_404(MessengerType, id=request.POST.get('messenger_type'))
  except MessengerType.DoesNotExist:
    return render(request, 'explorer/add_account.html', { 'error_message' : 'Missing account type' })

  login = request.POST.get('login');
  if login is None or len(login) < 1:
    return render(request, 'explorer/add_account.html', { 'error_message' : 'Account login should not be empty' })

  if messenger_type.id == 1:
    if not re.match(r"^\+\d+$", login):
      return render(request, 'explorer/add_account.html', { 'error_message' : 'Account login should contain only + and digits' })
  elif messenger_type.id == 2:
    if not re.match(r"^id\d+$", login):
      return render(request, 'explorer/add_account.html', { 'error_message' : 'Account login should be in format id\\d+' })

  try:
    account = Account.objects.get(user=request.user, name=login)
  except Account.DoesNotExist:
    account = Account()
    account.messenger_type = messenger_type
    account.user = request.user
    account.name = login
    account.save()

  if messenger_type.id == 1:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tl_client = TelegramClient(settings.TELETHON_SESSIONS_DIR + "/" + str(request.user.id) + "_" + login, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    tl_client.connect()  # Must return True, otherwise, try again

    with tl_client:
      if not tl_client.is_user_authorized():
        sent_code = tl_client.send_code_request(login)
        return redirect("explorer:telegram_sign_in", account_id=account.id, telegram_phone_hash=sent_code.phone_code_hash)

      account.signed_in = True
      account.save()
      return redirect("explorer:index")
  elif messenger_type.id == 2:
    account.signed_in = True
    account.save()
    return redirect("explorer:index")
  else:
    return render(request, 'explorer/add_account.html', { 'error_message' : 'Unsupported messenger type' })

@login_required
def telegram_sign_in(request, account_id, telegram_phone_hash):
  account = get_object_or_404(Account, user=request.user, id=account_id)
  login = account.name
  if not telegram_phone_hash:
    return redirect("explorer:add_account")

  context = {
    'account_id': account_id,
    'telegram_phone_hash': telegram_phone_hash,
  }

  if request.POST.get('submit') is None:
    return render(request, 'explorer/telegram_sign_in.html', context)

  telegram_code = request.POST.get('telegram_code')
  if telegram_code is None:
    context.update({ 'error_message' : 'Missing telegram code' })
    return render(request, 'explorer/telegram_sign_in.html', context)
  if not re.match(r"^\d+$", telegram_code):
    context.update({ 'error_message' : 'Telegram should not be empty and should contain only digits' })
    return render(request, 'explorer/telegram_sign_in.html', context)

  tl_client = TelegramClient(settings.TELETHON_SESSIONS_DIR + "/" + str(request.user.id) + "_" + login, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  rc = tl_client.connect()  # Must return True, otherwise, try again
  # .sign_in() may raise PhoneNumberUnoccupiedError
  # In that case, you need to call .sign_up() to get a new account
  telegram_user = tl_client.sign_in(phone=login, code=telegram_code, phone_code_hash=telegram_phone_hash)

  if telegram_user and isinstance(telegram_user, TelegramUser):
    account.signed_in = True
    account.save()
    return redirect('explorer:index')

  # TODO: return good error page
  return HttpResponse("Failed to sign in into telegram, please try again")

@login_required
def list_remote_chats(request, account_id):
  account = get_object_or_404(Account, user=request.user, id=account_id)
  chats = []

  if account.messenger_type.id == 1:
    telethon_session_path = settings.TELETHON_SESSIONS_DIR + "/" + str(request.user.id) + "_" + account.name
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tl_client = TelegramClient(telethon_session_path, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    tl_client.connect()
    if not tl_client.is_user_authorized():
      return redirect("explorer:add_account")

    with tl_client:
      result = ""
      xstr = lambda s: s or ""

      limit = 5
      offset_date = None

      for dialog in tl_client.iter_dialogs():
        print(dialog.id)

        if dialog.is_user:
          user = dialog.entity
          title = xstr(user.first_name) + " " + xstr(user.last_name)
          chat = {
            'title': title,
            'type_str': "User",
            'remote_id': user.id,
            'remote_type': 1,
            'original_title': title,
          }
        elif dialog.is_group:
          chat = dialog.entity
          title = chat.title
          chat = {
            'title': title,
            'type_str': "Chat",
            'remote_id': chat.id,
            'remote_type': 2,
            'original_title': title,
          }
        elif dialog.is_channel:
          channel = dialog.entity
          title = channel.title
          chat = {
            'title': title,
            'type_str': "Channel",
            'remote_id': channel.id,
            'remote_type': 3,
            'original_title': title,
          }
        else:
          title = "Unknown type:" + pprint.pformat(dialog.entity)
          chat = {
            'title': title,
            'remote_id': 0,
            'original_title': title,
          }

        chats.append(chat)
  elif account.messenger_type.id == 2:
          chats.append({
            'title': 'AAA',
            'type_str': "Chat",
            'remote_id': 1000,
            'remote_type': 2,
            'original_title': 'AAA',
          })
  else:
    return render(request, 'explorer/list_remote_chats.html', { 'error_message' : 'Unsupported messenger type' })

  context = {
    'account_id': account.id,
    'account_login': account.name,
    'chats': chats
  }

  return render(request, 'explorer/list_remote_chats.html', context)

@login_required
def import_remote_chat(request, account_id, remote_id, remote_type):
  try:
    chat = Chat.objects.get(user=request.user, account_id=account_id, remote_id=remote_id)
    message = "This chat is already imported #%d \"%s\", updating it " % (chat.id, chat.title)
    messages.add_message(request, messages.INFO, message)
  except Chat.DoesNotExist:
    account = get_object_or_404(Account, user=request.user, id=account_id)
    chat_type = get_object_or_404(ChatType, id=remote_type)
    title = request.GET.get('title', '')
    original_title = request.GET.get('original_title', '')
    chat = Chat()
    chat.remote_id = remote_id
    chat.remote_type = chat_type.id
    chat.user = request.user
    chat.account = account
    chat.title = title
    chat.original_title = original_title
    chat.save()

  new_update_generation = chat.update_generation + 1
  affected_rows = Chat.objects.filter(id=chat.id, is_being_updated=False, update_generation=chat.update_generation).update(
    update_generation=new_update_generation,
    is_being_updated=True,
    update_started_at=datetime.now()
  )

  if affected_rows != 1:
    raise RuntimeError("Cannot initiate update of chat, somebody else has already updated it, please try again")

  sync_telegram_chat.delay(chat.id, new_update_generation)

  return redirect('explorer:index')

@login_required
def explore_chat(request, chat_id):
  chat = get_object_or_404(Chat, id=chat_id, user=request.user)
  messages = Message.objects.filter(chat_id=chat.id).all()
  with connection.cursor() as cursor:
      case = "CASE %s END AS daytime" % " ".join(['WHEN daytime = %s THEN "%s"' % (x[0], x[1]) for x in Message.DAYTIME_CHOICES])
      sql = 'SELECT date(date), %s, COUNT(*) FROM %s' % (case, Message()._meta.db_table)
      sql += ' WHERE chat_id = %s AND author_name not in ("Бот-менеджер", "Juggler Search") GROUP BY date(date), daytime'
      cursor.execute(sql, [chat.id])
      stats = cursor.fetchall()
  context = {
    'chat': chat,
    'chat_messages': messages,
    'stats': json.dumps(stats)
  }

  return render(request, 'explorer/explore_chat.html', context)
