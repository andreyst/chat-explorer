from django.contrib import admin

from .models import ChatAccount, MessengerType, ChatChannel, ChannelType, ChatMessage

admin.site.register(ChatAccount)
admin.site.register(MessengerType)
admin.site.register(ChatChannel)
admin.site.register(ChannelType)
admin.site.register(ChatMessage)
