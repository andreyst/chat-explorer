from django.db import models
from django.contrib.auth.models import User

class MessengerType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
      return self.name

class ChannelType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
      return self.name

class ChatAccount(models.Model):
    id = models.AutoField(primary_key=True)
    messenger_type = models.ForeignKey(MessengerType, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    login = models.CharField(max_length=32)
    signed_in = models.BooleanField(default=False)

    def __str__(self):
      return self.login

class ChatChannel(models.Model):
    id = models.AutoField(primary_key=True)
    ttype = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    chat_account = models.ForeignKey(ChatAccount, on_delete=models.CASCADE, default=0)
    remote_id = models.BigIntegerField(default=0)
    title = models.CharField(max_length=4096, default='')
    remote_title = models.CharField(max_length=4096, default='')

    def __str__(self):
      return str("%d (%s)" % (self.id, self.title))

class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    remote_id = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    chat_account = models.ForeignKey(ChatAccount, on_delete=models.CASCADE, default=0)
    chat_channel = models.ForeignKey(ChatChannel, on_delete=models.CASCADE, default=0)
    date = models.DateTimeField()
    from_id = models.BigIntegerField(default=0)
    author_name = models.CharField(max_length=4096, default='')
    text = models.CharField(max_length=4096)

    def __str__(self):
      text = (self.text[:75] + '..') if len(self.text) > 75 else self.text
      res = "[%s] %s: %s" % (self.date.isoformat(), self.author_name, text)
      return res
