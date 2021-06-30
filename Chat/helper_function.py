from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Chat
from Profile.models import Profile

User = get_user_model()

# this is the thing that you gonna work for tommorow.
def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.all()

def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Profile, user=user)

# You havent solve the problem yet J, work for this tommorow okay   
def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)

def message_filter(request):
    chat_id = request.GET.get("id")
    limit = request.GET.get("limit")
    offset = request.GET.get('offset')
    chat = get_object_or_404(Chat, id=chat_id)
    return chat.messages.all()[int(offset): int(offset) + int(limit)]