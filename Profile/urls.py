from django.urls import path

from .api import (
    profile_detail_api_view,  
    other_user_friend_action, 
    FanPageListAIPView,
    RequestListAPIView, 
    FriendListAPIView, 
    FollowerListAPIView, 
    FollowingListAPIView,
    ProfileUpdateApiView
    )

urlpatterns = [
    path('api/<str:username>/', profile_detail_api_view),
    path('api/<str:username>/follow/', profile_detail_api_view),
    path('api/<int:id>/other-friend/', other_user_friend_action),
    path('api/<str:slug>/fanpage/', FanPageListAIPView.as_view()),
    path('api/request/list/', RequestListAPIView.as_view()),
    path('api/friends/list/', FriendListAPIView.as_view()),
    path('api/follower/list/', FollowerListAPIView.as_view()),
    path('api/following/list/', FollowingListAPIView.as_view()),
    path('api/following/list/', FollowingListAPIView.as_view()),
    path('api/<pk>/update/profile/', ProfileUpdateApiView.as_view()),
]

