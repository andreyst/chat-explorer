from .models import MessengerType, Account, ChatType, Chat, Message
from django.http import JsonResponse
import json
import random
import time
from django.contrib.auth.decorators import login_required

@login_required
def test(request):
  accounts = [
    { 'id': 1, 'name': "+79312010222", 'type': 'telegram' },
    { 'id': 2, 'name': "+11111111111", 'type': 'slack' },
    { 'id': 3, 'name': "+22222222222", 'type': 'facebook' },
    { 'id': 4, 'name': "+33333333333", 'type': 'vk' },
  ]
  if random.randint(0, 1):
    res = HttpResponse(json.dumps(accounts))
  else:
    res = HttpResponse(json.dumps(accounts), status=500)
  time.sleep(1)

  return res

@login_required
def accounts(request):
  query = Account.objects.filter(user=request.user).all()
  accounts = []
  for account in query:
    accounts.append({ 'id': account.id, 'name': account.name, 'messenger_type': account.messenger_type.id })

  res = JsonResponse({
    'accounts': accounts
  })
  res['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  return res