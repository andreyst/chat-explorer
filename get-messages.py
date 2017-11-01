from __future__ import print_function
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

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone = os.environ.get('PHONE')

client = TelegramClient('andreyst-test-bot', api_id, api_hash)
client.connect()  # Must return True, otherwise, try again

if not client.is_user_authorized():
    client.send_code_request(phone)
    # .sign_in() may raise PhoneNumberUnoccupiedError
    # In that case, you need to call .sign_up() to get a new account
    client.sign_in(phone, input('Enter code: '))

xstr = lambda s: s or ""

[ dialogs, entities ] = client.get_dialogs()
for dialog in dialogs:
  if isinstance(dialog.peer, PeerUser):
    user = client.get_entity(PeerUser(dialog.peer.user_id))
    pprint.pprint(xstr(user.first_name) + " " + xstr(user.last_name))
  elif isinstance(dialog.peer, PeerChannel):
    channel = client.get_entity(PeerChannel(dialog.peer.channel_id))
    pprint.pprint(channel.title)
  elif isinstance(dialog.peer, PeerChat):
    chat = client.get_entity(PeerChat(dialog.peer.chat_id))
    pprint.pprint(chat.title)
  else:
    print("Unknown type:")
    pprint.pprint(dialog.peer)

sys.exit(0)

# chat
lbops_private_chat = client.get_entity(PeerChannel(1077051540))
offset_id = 0
author_ids = set()
author_names = {}

while True:
  (total_messages_count, messages_slice, senders) = client.get_message_history(lbops_private_chat, limit=100, offset_id=offset_id)
  if len(messages_slice) == 0:
    break

  offset_id = messages_slice[-1].id
  eprint("%s, %s" % (messages_slice[-1].date, len(messages_slice)))

  for message in messages_slice:
    if not isinstance(message, Message):
      eprint("Skipping non-message %s" % pprint.pformat(message))
      continue

    if message.from_id not in author_ids:
      author = client.get_entity(PeerUser(message.from_id))
      author_name = author.first_name
      if author.last_name is not None:
        author_name += " " + author.last_name
      author_names[message.from_id] = author_name
      author_ids.add(message.from_id)

    author_name = author_names[message.from_id]
    print(json.dumps([message.id, message.date.isoformat(), message.from_id, author_name, message.message], ensure_ascii=False))

### to get all dialogs/users/chats
# dialogs = []
# users = []
# chats = []

# last_date = None
# chunk_size = 20
# while True:
#     result = client(GetDialogsRequest(
#                  offset_date=last_date,
#                  offset_id=0,
#                  offset_peer=InputPeerEmpty(),
#                  limit=chunk_size
#              ))
#     dialogs.extend(result.dialogs)
#     users.extend(result.users)
#     chats.extend(result.chats)
#     if not result.messages:
#         break
#     last_date = min(msg.date for msg in result.messages)
#     sleep(2)

# pprint.pprint(dialogs)
# pprint.pprint(users)
# pprint.pprint(chats)

# for chat in chats:
#   print("%s: %s" % (chat.id, chat.title))