from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import Message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import re

def index(request):
  chat_user_login = request.session.get('chat_user_login')
  if not chat_user_login:
    return redirect("explorer:login")

  client = TelegramClient(settings.TELETHON_SESSIONS_DIR + "/" + chat_user_login, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  rc = client.connect()  # Must return True, otherwise, try again

  result = ""
  xstr = lambda s: s or ""

  [ dialogs, entities ] = client.get_dialogs()
  for dialog in dialogs:
    if isinstance(dialog.peer, PeerUser):
      user = client.get_entity(PeerUser(dialog.peer.user_id))
      result += xstr(user.first_name) + " " + xstr(user.last_name) + "<br/>"
    elif isinstance(dialog.peer, PeerChannel):
      channel = client.get_entity(PeerChannel(dialog.peer.channel_id))
      result += channel.title + "<br/>"
    elif isinstance(dialog.peer, PeerChat):
      chat = client.get_entity(PeerChat(dialog.peer.chat_id))
      result += chat.title + "<br/>"
    else:
      result += "Unknown type:"
      result += pprint.pformat(dialog.peer)

  return HttpResponse(result)

def login(request):
  if request.POST.get('submit') is None:
    return render(request, 'explorer/login.html', {})

  chat_type = request.POST.get('chat_type')
  if chat_type is None:
    return render(request, 'explorer/login.html', { 'error_message' : 'Missing chat type' })

  chat_type = int(chat_type)

  chat_user_login = request.POST.get('chat_user_login');
  if chat_user_login is None or len(chat_user_login) < 1:
    return render(request, 'explorer/login.html', { 'error_message' : 'Empty chat user login' })
  if not re.match(r"^\+\d+$", chat_user_login):
    return render(request, 'explorer/login.html', { 'error_message' : 'Chat user login should contain only + and digits' })

  request.session['chat_type'] = chat_type
  request.session['chat_user_login'] = chat_user_login

  if chat_type == 1:
    client = TelegramClient(settings.TELETHON_SESSIONS_DIR + "/" + chat_user_login, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    rc = client.connect()  # Must return True, otherwise, try again

    if not client.is_user_authorized():
      sent_code = client.send_code_request(chat_user_login)
      request.session['telegram_phone_hash'] = sent_code.phone_code_hash
        # .sign_in() may raise PhoneNumberUnoccupiedError
        # In that case, you need to call .sign_up() to get a new account
      return redirect("explorer:telegram_sign_in")

    return redirect("explorer:index")
  else:
    return render(request, 'explorer/login.html', { 'error_message' : 'Unsupported chat type' })

def telegram_sign_in(request):
  chat_user_login = request.session.get('chat_user_login')
  telegram_phone_hash = request.session.get('telegram_phone_hash')
  if not chat_user_login or not telegram_phone_hash:
    return redirect("explorer:login")

  if request.POST.get('submit') is None:
    return render(request, 'explorer/telegram_sign_in.html', {})

  telegram_code = request.POST.get('telegram_code')
  if telegram_code is None:
    return render(request, 'explorer/telegram_sign_in.html', { 'error_message' : 'Missing telegram code' })
  if not re.match(r"^\d+$", telegram_code):
    return render(request, 'explorer/telegram_sign_in.html', {
      'error_message' : 'Telegram should not be empty and should contain only digits'
    })

  client = TelegramClient(settings.TELETHON_SESSIONS_DIR + "/" + chat_user_login, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  rc = client.connect()  # Must return True, otherwise, try again
  client.sign_in(phone=chat_user_login, code=telegram_code, phone_code_hash=telegram_phone_hash)

  return redirect("explorer:index")
