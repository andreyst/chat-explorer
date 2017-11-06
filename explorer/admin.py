from django.contrib import admin

from .models import MessengerType, Account, ChatType, Chat, Message

admin.site.register(MessengerType)
admin.site.register(Account)
admin.site.register(ChatType)
admin.site.register(Chat)
admin.site.register(Message)
