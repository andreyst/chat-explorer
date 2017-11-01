from django.db import models

class ChatUser(models.Model):
    phone = models.CharField(max_length=32)

    def __str__(self):
      return self.phone
