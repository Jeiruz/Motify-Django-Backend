
from django.urls import path

from .api import (
    PostCreateView,
    PostDetailAPIView,
    post_action_view,
    TagsFilterAPIView,
    UserLikeListAPIView,
    CommentListAPIView,
    UserPostAPIView,
    UserFeedAPIView,
    PostFilterAPIView,
    post_delete_view,
    LikedPostAPIView,
    AnonymousPostAPIView,
    ForYouPostAPIView
    )

from .category_filter import category_filter

urlpatterns = [
    path('api/post/create/', PostCreateView.as_view(), name="create"),
    path('api/post/<str:slug>/detail/', PostDetailAPIView.as_view(), name="detail"),
    path('api/post/user_feed/', UserFeedAPIView.as_view(), name="user_feed"),
    path('api/post/action/', post_action_view, name="action"),
    path('api/post/like-list/', UserLikeListAPIView.as_view(), name="like_list"),
    path('api/post/<str:slug>/comments/', CommentListAPIView.as_view(), name="comment_list"),
    path('api/user/list/', UserPostAPIView.as_view(), name="user_post"),
    path('api/category/filter/', category_filter, name="category_filter"),
    path('api/post/filter/', PostFilterAPIView.as_view(), name="post_filter"),
    path('api/post/<int:post_id>/delete/', post_delete_view, name="post_delete"),
    path('api/post/liked/', LikedPostAPIView.as_view(), name="liked_post"),
    path('api/post/anonymous/', AnonymousPostAPIView.as_view(), name="liked_post"),
    path('api/post/tags/filter/', TagsFilterAPIView.as_view(), name="tags_filter"),
    path('api/post/for_you/', ForYouPostAPIView.as_view(), name="for_you")
]
