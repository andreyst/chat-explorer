from django.db import models
from django.contrib.auth.models import User

class MessengerType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
      return self.name

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    messenger_type = models.ForeignKey(MessengerType, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    login = models.CharField(max_length=32)
    signed_in = models.BooleanField(default=False)

    def __str__(self):
      return self.login

class ChatType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
      return self.name

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    remote_id = models.BigIntegerField(default=0)
    remote_type = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=0)
    title = models.CharField(max_length=4096, default='')
    original_title = models.CharField(max_length=4096, default='')

    def __str__(self):
      return str("%d (%s)" % (self.id, self.title))

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    remote_id = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=0)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, default=0)
    date = models.DateTimeField()
    from_id = models.BigIntegerField(default=0)
    author_name = models.CharField(max_length=4096, default='')
    text = models.CharField(max_length=4096)

    def __str__(self):
      text = (self.text[:75] + '..') if len(self.text) > 75 else self.text
      res = "[%s] %s: %s" % (self.date.isoformat(), self.author_name, text)
      return res

    class Meta:
      indexes = [
          models.Index(fields=['chat_id', 'date', 'remote_id']),
      ]
