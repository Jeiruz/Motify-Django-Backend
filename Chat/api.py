from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from .models import Chat, Message
from .helper_function import get_user_contact, message_filter
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()


class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = Chat.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset


# Don't delete this just in case
# class ChatDetailView(RetrieveAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.AllowAny, )
class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )



class ChatScrollListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = Chat.objects.all()
        username = self.request.query_params.get('username', None)
        offset = self.request.query_params.get('offset', None)
        limit = self.request.query_params.get('limit', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()[int(offset): int(offset) + int(limit)]
        return queryset 


class ChatDetailView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        chat_id = self.request.query_params.get("chat_id", None)
        queryset = Chat.objects.filter(id=chat_id)
        return queryset


# class MessageScrollListView(ListAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = (permissions.AllowAny, )

#     def get_queryset(self):
#         queryset = Message.objects.all()
#         offset = self.request.query_params.get('offset', None)
#         limit = self.request.query_params.get('limit', None)
#         chat_id = self.request.query_params.get('chat_id', None)
#         if int(offset) < get_last_10_messages(chat_id).count():
#             queryset = get_last_10_messages(chat_id)[int(offset): int(offset) + int(limit)]
#         return queryset
            


class MessageListAPIView(ListAPIView): 
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qs = message_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response(serializer.data)