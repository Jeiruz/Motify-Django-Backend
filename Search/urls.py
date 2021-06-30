from .api import (
        profile_search_filter, 
        search_filter, 
        notification, 
        likes_notification, 
        follower_notification, 
        request_notification,
        no_following_yet
        )
from django.urls import path

urlpatterns = [
        path('api/search/profile/', profile_search_filter),
        path('api/search/model/', search_filter),
        path('api/notification/user/', notification),
        path('api/likes/notification/user/', likes_notification),
        path('api/follower/notification/user/', follower_notification),
        path('api/request/notification/user/', request_notification),
        path('api/post/no_following/', no_following_yet),
]

