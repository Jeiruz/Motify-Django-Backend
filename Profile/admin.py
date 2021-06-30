from django.contrib import admin

from .models import Profile, FriendRelation


admin.site.register(Profile)
admin.site.register(FriendRelation)