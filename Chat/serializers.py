from rest_framework import serializers

from django.shortcuts import render, get_object_or_404
from .models import Chat, ChatList, Message
from .helper_function import get_user_contact, get_current_chat
from Profile.models import Profile

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Message
        fields = ["id", "content", "timestamp", "username"] 

    def create(self, validated_data):
        request = self.context["request"]
        user = request.data["user"]
        content = request.data["content"]
        chat_id = request.data["chat_id"]
        user_contact = get_user_contact(user)
        message = Message.objects.create(
            contact=user_contact, 
            content=content)
        current_chat = get_current_chat(chat_id)
        current_chat.messages.add(message)
        current_chat.save()
        return message
    
    def get_username(self, obj):
        return obj.contact.user.username



class ChatListSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChatList
        fields = ["id", "username", "image"]

    def get_username(self, obj):
        return obj.username

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        
        return image

class ProfileSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ChatSerializer(serializers.ModelSerializer):
    chat_count = serializers.SerializerMethodField(read_only=True)
    user_list = ChatListSerializers(read_only=True,many=True, source="chat_list")
    participants = ProfileSerializer(many=True)
    messages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'chat_count', 'chat_list', 'participants', 'user_list', 'messages')
        read_only = ('id')

    def get_chat_count(self, obj):
        return obj.chat_list.count()

    def create(self, validated_data):
        request = self.context["request"]
        users = request.data['id']
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        sender = request.data['sender']
        content = request.data['content']
        user_contact = get_user_contact(sender)
        for username in participants:
            contact = get_user_contact(username)
            chat.participants.add(contact)
        for user in users:
            chat.chat_list.add(user)
        message_model = Message.objects.create(
            contact=user_contact,
            content=content
        )
        chat.messages.add(message_model)
        chat.save()
        return chat

    def get_messages(self, obj):
        chat = get_object_or_404(Chat, id=obj.id)
        c_qs = chat.messages.order_by('-timestamp').all()[0:1]
        messages = MessageSerializer(c_qs, many=True).data
        return messages

