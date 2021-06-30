from django.urls import path

from .api import (
    ChatListView,
    ChatDetailView,
    ChatCreateView,
    ChatUpdateView,
    ChatDeleteView,
    ChatScrollListView,
    MessageCreateView,
    MessageListAPIView
)

app_name = 'chat'

urlpatterns = [
    path('chat/', ChatListView.as_view()),
    path('chat/create/', ChatCreateView.as_view()),
    path('chat/own_chat/', ChatDetailView.as_view()),
    path('chat/<pk>/update/', ChatUpdateView.as_view()),
    path('chat/<pk>/delete/', ChatDeleteView.as_view()),
    path('chat/list/', ChatScrollListView.as_view()),
    path('chat/create/message/', MessageCreateView.as_view()),
    path('chat/list/message/', MessageListAPIView.as_view())
]
