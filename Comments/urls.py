
from django.urls import path

from .api import (
    CommentCreateAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    CommentReplyListAPIView
    )

urlpatterns = [
    path('api/comments/create/', CommentCreateAPIView.as_view(), name="create"),
    path('api/comments/detail/<int:pk>/', CommentDetailAPIView.as_view(), name="thread"),
    path('api/comments/list/', CommentListAPIView.as_view(), name="comment_list"),
    path('api/comments/replies/', CommentReplyListAPIView.as_view(), name="comment_reply")
]
