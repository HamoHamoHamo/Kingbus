from django.db import models
from user.models import User

# Create your models here.

class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)


class ChatroomList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user')
    driverorcompany = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_driverorcompany')
    chatroom = models.CharField(max_length=255)

