from django.db import models
from rest_framework import serializers

from .models import Profile, FriendRequestRelation, FollowerRelation, FriendRelation
from Accounts.serializers import UserSerializer
from Posts.models import Post
from Posts.serializers import PostSerializers
from drf_extra_fields.fields import Base64ImageField

class FriendRelationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FriendRelation
        fields = ["id", "username", "image"]
    
    def get_username(self, obj):
        return obj.user.username

    def get_image(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        
        return image

    def get_id(self, obj):
        return obj.user.id

class FriendRequestRelationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    model_type = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FriendRequestRelation
        fields = ["id", "user", "image", "timestamp", "model_type"]

    def get_user(self, obj):
        return obj.user.username

    def get_model_type(self, obj):
        return "request"
    
    def get_image(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        return image

class FollowerRelationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    model_type = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FollowerRelation
        fields = ["user", "model_type", "timestamp", "image"]

    def get_user(self, obj):
        return obj.username
    
    def get_model_type(self, obj):
        return "follower"
    
    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image




class PublicProfileSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    friend_count = serializers.SerializerMethodField(read_only=True)
    is_request = serializers.SerializerMethodField(read_only=True)
    user_follower = FollowerRelationSerializer(source="following_count", read_only=True, many=True)
    is_friend = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    cover_photo = serializers.SerializerMethodField(read_only=True)
    post = serializers.SerializerMethodField(read_only=True)
    friends = serializers.SerializerMethodField(read_only=True)
    follower = serializers.SerializerMethodField(read_only=True)
    background_image = Base64ImageField(required=False)
    date_joined = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            "bio",
            "location",
            "follower_count",
            "following_count",
            "is_following",
            "friend_count",
            "is_request",
            "user_follower",
            'is_friend',
            "username",
            "id",
            "image",
            "cover_photo",
            "post",
            "friends",
            "follower",
            "background_image",
            "date_joined",
            "background_color",
            "color",
            "images",
            "third_color"
        ]
    
    def get_is_following(self, obj):
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following

    def get_date_joined(self, obj):
        return obj.user.date_joined

    def get_is_request(self, obj):
        is_request = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_request = user in obj.friend_request.all()
        return is_request

    def get_is_friend(self, obj):
        is_friend = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_friend = user in obj.friends.all()
        return is_friend
    
    
    def get_following_count(self, obj):
        return obj.user.following.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_friend_count(self, obj):
        return obj.friends.count()

    def get_username(self, obj):
        return obj.user.username
    
    def get_image(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        
        return image

    def get_id(self, obj):
        return obj.user.id

    def get_cover_photo(self, obj):
        try:
            image = obj.background_image.url
        except:
            image = None
        return image

    def get_post(self, obj):
        f_qs = Post.objects.filter(user=obj.user)[0:8]
        fanpage = PostSerializers(f_qs, many=True, context={ "request": self.context["request"]}).data
        return fanpage
    
    def get_friends(self, obj):
        qs = FriendRelation.objects.filter(profile=obj)[0:6]
        profile = FriendRelationSerializer(qs, many=True).data
        return profile
    
    def get_follower(self, obj):
        follower = FollowerRelationSerializer(obj.followers.all()[0:6], many=True).data
        return follower
    
    def get_images(self, obj):
        f_qs = Post.objects.filter(user=obj.user)
        images = PostSerializers(f_qs, many=True, context={ "request": self.context["request"]}).data
        array = []
        for image in images:
            if image["image"] == None:
                pass
            else:
                array.append(image)
        return array


class ProfilePostListSerializers(serializers.ModelSerializer):
    post = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'post'
        ]
    def get_post(self, obj):
        f_qs = Post.objects.filter_by_instance(obj)
        fanpage = PostSerializers(f_qs, many=True).data
        return fanpage

class ProfileSlugSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'slug'
        ]


# class FollowingListSerializer(serializers.ModelSerializer):
#     username = serializers.SerializerMethodField(read_only=True)
#     image = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Profile
#         fields = [
#             "username",
#             "id",
#             "image",
#         ]
    
#     def get_username(self, obj):
#         return obj.user.username
    
#     def get_image(self, obj):
#         try:
#             image = obj.user.image.url
#         except:
#             image = None
        
#         return image

 

class FollowingListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FriendRelation
        fields = ["id", "username", "image"]
    
    def get_username(self, obj):
        return obj.user.username

    def get_image(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        
        return image

    def get_id(self, obj):
        return obj.user.id