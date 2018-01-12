from telethon import TelegramClient
from telethon.tl.types import User as TelegramUser
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import MessengerType, Account, ChatType, Chat, Message
import pprint
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .tasks import sync_telegram_chat
from django.db import connection
import json

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
  return render(request, 'explorer/list_accounts.html', { 'accounts': accounts })

@login_required
def add_account(request):
  if request.POST.get('submit') is None:
    return render(request, 'explorer/add_account.html', {})

  try:
    messenger_type = get_object_or_404(MessengerType, id=request.POST.get('messenger_type'))
  except MessengerType.DoesNotExist:
    return render(request, 'explorer/add_account.html', { 'error_message' : 'Missing chat type' })

  login = request.POST.get('login');
  if login is None or len(login) < 1:
    return render(request, 'explorer/add_account.html', { 'error_message' : 'Chat login should not be empty' })
  if not re.match(r"^\+\d+$", login):
    return render(request, 'explorer/add_account.html', { 'error_message' : 'Chat login should contain only + and digits' })

  try:
    account = Account.objects.get(user=request.user, login=login)
  except Account.DoesNotExist:
    account = Account()
    account.messenger_type = messenger_type
    account.user = request.user
    account.login = login
    account.save()

  if messenger_type.id == 1:
    tl_client = TelegramClient(settings.TELETHON_SESSIONS_DIR + "/" + str(request.user.id) + "_" + login, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    rc = tl_client.connect()  # Must return True, otherwise, try again

    if not tl_client.is_user_authorized():
      sent_code = tl_client.send_code_request(login)
      return redirect("explorer:telegram_sign_in", account_id=account.id, telegram_phone_hash=sent_code.phone_code_hash)

    account.signed_in = True
    account.save()
    return redirect("explorer:index")
  else:
    return render(request, 'explorer/add_account.html', { 'error_message' : 'Unsupported messenger type' })

@login_required
def telegram_sign_in(request, account_id, telegram_phone_hash):
  account = get_object_or_404(Account, user=request.user, id=account_id)
  login = account.login
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

  telethon_session_path = settings.TELETHON_SESSIONS_DIR + "/" + str(request.user.id) + "_" + account.login
  tl_client = TelegramClient(telethon_session_path, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  rc = tl_client.connect()  # Must return True, otherwise, try again
  if rc is not True:
    redirect("explorer:add_account")

  result = ""
  xstr = lambda s: s or ""
  chats = []

  limit = 5
  offset_date = None

  while limit > 0:
    limit -= 1
    result = tl_client(GetDialogsRequest(
                                        offset_date=offset_date,
                                        offset_id=0,
                                        offset_peer = InputPeerEmpty(),
                                        limit=10
                                      ))

    for dialog in result.dialogs:
      if isinstance(dialog.peer, PeerUser):
        user = tl_client.get_entity(PeerUser(dialog.peer.user_id))
        title = xstr(user.first_name) + " " + xstr(user.last_name)
        chat = {
          'title': title,
          'type_str': "User",
          'remote_id': dialog.peer.user_id,
          'remote_type': 1,
          'original_title': title,
        }
      elif isinstance(dialog.peer, PeerChat):
        chat = tl_client.get_entity(PeerChat(dialog.peer.chat_id))
        title = chat.title
        chat = {
          'title': title,
          'type_str': "Chat",
          'remote_id': dialog.peer.chat_id,
          'remote_type': 2,
          'original_title': title,
        }
      elif isinstance(dialog.peer, PeerChannel):
        channel = tl_client.get_entity(PeerChannel(dialog.peer.channel_id))
        title = channel.title
        chat = {
          'title': title,
          'type_str': "Channel",
          'remote_id': dialog.peer.channel_id,
          'remote_type': 3,
          'original_title': title,
        }
      else:
        title = "Unknown type:" + pprint.pformat(dialog.peer)
        chat = {
          'title': title,
          'remote_id': 0,
          'original_title': title,
        }

      chats.append(chat)

    if not result.messages:
        break

    offset_date = min(msg.date for msg in result.messages)

  context = {
    'account_id': account.id,
    'account_login': account.login,
    'chats': chats
  }

  return render(request, 'explorer/list_remote_chats.html', context)

@login_required
def import_remote_chat(request, account_id, remote_id, remote_type):
  try:
    chat = Chat.objects.get(user=request.user, account_id=account_id, remote_id=remote_id)
    message = "This chat is already imported #%d \"%s\" " % (chat.id, chat.title)
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

  sync_telegram_chat.delay(chat.id)

  return redirect('explorer:index');

@login_required
def explore_chat(request, chat_id):
  chat = get_object_or_404(Chat, id=chat_id, user=request.user)
  messages = Message.objects.filter(chat_id=chat.id).all()
  with connection.cursor() as cursor:
      case = "CASE %s END AS daytime" % " ".join(['WHEN daytime = %s THEN "%s"' % (x[0], x[1]) for x in Message.DAYTIME_CHOICES])
      sql = 'SELECT date(date), %s, COUNT(*) FROM %s' % (case, Message()._meta.db_table)
      sql += ' WHERE chat_id = %s GROUP BY date(date), daytime'
      cursor.execute(sql, [chat.id])
      stats = cursor.fetchall()
  context = {
    'chat': chat,
    'chat_messages': messages,
    'stats': json.dumps(stats)
  }

  return render(request, 'explorer/explore_chat.html', context)
