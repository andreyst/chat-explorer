from telethon import TelegramClient
from telethon.tl.types import User as TelegramUser
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import Message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import ChatAccount, MessengerType, ChatChannel, ChannelType
import pprint
from django.shortcuts import get_object_or_404
from django.contrib import messages

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
  saved_channels = ChatChannel.objects.filter(user=request.user).all()
  # return HttpResponse(pprint.pformat(chat_accounts))
  return render(request, 'explorer/index.html', { 'saved_channels': saved_channels })

@login_required
def list_chat_accounts(request):
  chat_accounts = ChatAccount.objects.filter(user=request.user).all()
  return render(request, 'explorer/list_chat_accounts.html', { 'chat_accounts': chat_accounts })

@login_required
def list_chat_channels(request, chat_account_id):
  chat_account = get_object_or_404(ChatAccount, user=request.user, id=chat_account_id)

  telethon_session_path = settings.TELETHON_SESSIONS_DIR + "/" + chat_account.login
  client = TelegramClient(telethon_session_path, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  rc = client.connect()  # Must return True, otherwise, try again

  result = ""
  xstr = lambda s: s or ""
  chat_channels = []

  [ dialogs, entities ] = client.get_dialogs()
  for dialog in dialogs:
    if isinstance(dialog.peer, PeerUser):
      user = client.get_entity(PeerUser(dialog.peer.user_id))
      title = xstr(user.first_name) + " " + xstr(user.last_name)
      chat_channel = {
        'title': title,
        'type_str': "(user)",
        'remote_id': dialog.peer.user_id,
        'remote_type': 1,
        'remote_title': title,
      }
    elif isinstance(dialog.peer, PeerChat):
      chat = client.get_entity(PeerChat(dialog.peer.chat_id))
      title = chat.title
      chat_channel = {
        'title': title,
        'type_str': "(chat)",
        'remote_id': dialog.peer.chat_id,
        'remote_type': 2,
        'remote_title': title,
      }
    elif isinstance(dialog.peer, PeerChannel):
      channel = client.get_entity(PeerChannel(dialog.peer.channel_id))
      title = channel.title
      chat_channel = {
        'title': title,
        'type_str': "(channel)",
        'remote_id': dialog.peer.channel_id,
        'remote_type': 3,
        'remote_title': title,
      }
    else:
      title = "Unknown type:" + pprint.pformat(dialog.peer)
      chat_channel = {
        'title': title,
        'remote_id': 0,
        'remote_title': title,
      }

    chat_channels.append(chat_channel)

  context = {
    'chat_account_id': chat_account.id,
    'chat_channels': chat_channels
  }

  return render(request, 'explorer/list_chat_channels.html', context)

@login_required
def add_chat_account(request):
  if request.POST.get('submit') is None:
    return render(request, 'explorer/add_chat_account.html', {})

  chat_type = request.POST.get('chat_type')
  if chat_type is None:
    return render(request, 'explorer/add_chat_account.html', { 'error_message' : 'Missing chat type' })

  messenger_type = get_object_or_404(MessengerType, id=chat_type)

  chat_login = request.POST.get('chat_login');
  if chat_login is None or len(chat_login) < 1:
    return render(request, 'explorer/add_chat_account.html', { 'error_message' : 'Chat login should not be empty' })
  if not re.match(r"^\+\d+$", chat_login):
    return render(request, 'explorer/add_chat_account.html', { 'error_message' : 'Chat login should contain only + and digits' })

  try:
    db_chat_account = ChatAccount.objects.get(user=request.user, login=chat_login)
  except ChatAccount.DoesNotExist:
    db_chat_account = ChatAccount()
    db_chat_account.messenger_type = messenger_type
    db_chat_account.user = request.user
    db_chat_account.login = chat_login
    db_chat_account.save()

  if chat_type == 1:
    client = TelegramClient(settings.TELETHON_SESSIONS_DIR + "/" + chat_login, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
    rc = client.connect()  # Must return True, otherwise, try again

    if not client.is_user_authorized():
      sent_code = client.send_code_request(chat_login)
      request.session['telegram_phone_hash'] = sent_code.phone_code_hash
        # .sign_in() may raise PhoneNumberUnoccupiedError
        # In that case, you need to call .sign_up() to get a new account
      return redirect("explorer:telegram_sign_in", chat_login=chat_login, telegram_phone_hash=telegram_phone_hash)

    db_chat_account.signed_in = True
    db_chat_account.save()
    return redirect("explorer:index")
  else:
    return render(request, 'explorer/add_chat_account.html', { 'error_message' : 'Unsupported chat type' })

@login_required
def telegram_sign_in(request, chat_account_id, telegram_phone_hash):
  chat_account = get_object_or_404(ChatAccount, user=request.user, id=chat_account_id)
  if not chat_login or not telegram_phone_hash:
    return redirect("explorer:add_chat_account")

  if request.POST.get('submit') is None:
    return render(request, 'explorer/telegram_sign_in.html', {})

  telegram_code = request.POST.get('telegram_code')
  if telegram_code is None:
    return render(request, 'explorer/telegram_sign_in.html', { 'error_message' : 'Missing telegram code' })
  if not re.match(r"^\d+$", telegram_code):
    return render(request, 'explorer/telegram_sign_in.html', {
      'error_message' : 'Telegram should not be empty and should contain only digits'
    })

  client = TelegramClient(settings.TELETHON_SESSIONS_DIR + "/" + chat_login, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
  rc = client.connect()  # Must return True, otherwise, try again
  telegram_user = client.sign_in(phone=chat_login, code=telegram_code, phone_code_hash=telegram_phone_hash)

  if telegram_user and isinstance(telegram_user, TelegramUser):
    db_chat_account.signed_in = True
    db_chat_account.save()
    return redirect('explorer:index')

  # TODO: return good error page
  return HttpResponse("Failed to sign in into telegram, please try again")

@login_required
def save_channel(request, chat_account_id, remote_id, remote_type):
  try:
    chat_channel = ChatChannel.objects.get(user=request.user, chat_account_id=chat_account_id, remote_id=remote_id)
    message = "This channel is already added as #%d \"%s\" " % (chat_channel.id, chat_channel.title)
    messages.add_message(request, messages.INFO, message)
  except ChatChannel.DoesNotExist:
    chat_account = get_object_or_404(ChatAccount, user=request.user, id=chat_account_id)
    channel_type = get_object_or_404(ChannelType, id=remote_type)
    title = request.GET.get('title', '')
    remote_title = request.GET.get('remote_title', '')
    chat_channel = ChatChannel()
    chat_channel.user = request.user
    chat_channel.ttype = channel_type.id
    chat_channel.chat_account = chat_account
    chat_channel.remote_id = remote_id
    chat_channel.title = title
    chat_channel.remote_title = remote_title
    chat_channel.save()

  return redirect('explorer:index');