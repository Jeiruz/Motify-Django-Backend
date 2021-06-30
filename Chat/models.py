# from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from Profile.models import Profile

User = settings.AUTH_USER_MODEL
        
class Message(models.Model):
    contact = models.ForeignKey(Profile, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.contact.user.username

class ChatList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Chat", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    participants = models.ManyToManyField(Profile, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)
    chat_list = models.ManyToManyField(User, related_name='chat_list', through=ChatList)

    def __str__(self):
        return "{}".format(self.pk)










# Do this J just in case your mind has change

# from django.contrib.auth import get_user_model
# from django.db import models

# User = get_user_model()

# class Contact(models.Model):
#     user = models.OneToOneField(User, related_name='contacts', on_delete=models.CASCADE)
#     chat = models.ForeignKey("Chat", on_delete=models.CASCADE)
#     message = models.ForeignKey("Message", on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username

# class Message(models.Model):
#     contacts = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.contact.user.username

# class ChatList(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     profile = models.ForeignKey("Chat", on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

# class Chat(models.Model):
#     participants = models.ManyToManyField(User, related_name='chats', through=Contact)
#     messages = models.ManyToManyField(Message, blank=True)
#     chat_list = models.ManyToManyField(User, related_name='chat_list', through=ChatList)

#     def __str__(self):
#         return "{}".format(self.pk)