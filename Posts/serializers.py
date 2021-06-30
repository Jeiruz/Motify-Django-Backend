from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.conf import settings
from Comments.models import Comment
from Comments.serializers import CommentSerializers
from drf_extra_fields.fields import Base64ImageField

from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    Serializer,
    IntegerField,
    CharField,
    )

from .models import Post, PostLike
from Accounts.serializers import UserSerializer

User = get_user_model()
SNIPPET_ACTION_OPTIONS = settings.SNIPPET_ACTION_OPTIONS

post_detail_url = HyperlinkedIdentityField(
    view_name='detail',
    lookup_field="slug",
)


class PostActionSerializer(Serializer):
    id = IntegerField()
    action = CharField()
    content = CharField(allow_blank=True, required=False)

    def validate_action(self, value):

        value = value.lower().strip()
        if not value in SNIPPET_ACTION_OPTIONS:
            raise ValidationError("This is not a valid action")
        return value

class PostParentSerializers(ModelSerializer):
    username = SerializerMethodField(read_only=True)
    image = SerializerMethodField(read_only=True)
    user_pic = SerializerMethodField(read_only=True)
    likes = SerializerMethodField(read_only=True)
    parent = SerializerMethodField(read_only=True)


    class Meta:
        model = Post
        fields = ["id", "content", "username", "slug", "image", "user_pic", "likes", "parent"]

    def get_username(self, obj):
        return obj.user.username

    
    def get_user_pic(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        
        return image

    def get_parent(self, obj):
        return None

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_likes(self, obj):
        return obj.likes.count()


    

class UserLikeSerializer(ModelSerializer):
    username = SerializerMethodField(read_only=True)
    image = SerializerMethodField(read_only=True)

    class Meta:
        model = PostLike
        fields = ["id", "username", "date", "image"]

    def get_username(self, obj):
        return obj.user.username

    def get_image(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        return image
    

class PostCreateSerializer(ModelSerializer):
    image = Base64ImageField(required=False)
    class Meta:
        model = Post
        fields = [
            "image",
            "content",
            "user",
        ]

class PostSerializers(ModelSerializer):
    url = post_detail_url
    likes = SerializerMethodField(read_only=True)
    is_liked = SerializerMethodField(read_only=True)
    username = SerializerMethodField(read_only=True)
    parent = PostParentSerializers(read_only=True)
    image = SerializerMethodField(read_only=True)
    user_pic = SerializerMethodField(read_only=True)
    comment_count = SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'parent',
            'content',
            'timestamp',
            'username',
            'is_liked',
            'image',
            'slug',
            'likes',
            'url',
            'user_pic',
            'comment_count'
        ]

    def get_username(self, obj):
        return obj.user.username

    def get_is_liked(self, obj):
        is_liked = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_liked = user in obj.likes.all()
        return is_liked

    def get_likes(self, obj):
        return obj.likes.count()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comment_count(self, obj):
        return Comment.objects.filter_by_instance(obj).count()

    def get_user_pic(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        
        return image


class CommentListSerializers(ModelSerializer):
    comments = SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id',
            'comments'
        ]
    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializers(c_qs, many=True).data
        return comments

class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    likes = SerializerMethodField(read_only=True)
    is_liked = SerializerMethodField(read_only=True)
    username = SerializerMethodField(read_only=True)
    parent = PostParentSerializers(read_only=True)
    image = SerializerMethodField(read_only=True)
    user_pic = SerializerMethodField(read_only=True)
    comment_count = SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'timestamp',
            'username',
            'is_liked',
            'image',
            'slug',
            'likes',
            'url',
            'user_pic',
            'comment_count'
        ]
        
    def get_username(self, obj):
        return obj.user.username

    def get_is_liked(self, obj):
        is_liked = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_liked = user in obj.likes.all()
        return is_liked

    def get_likes(self, obj):
        return obj.likes.count()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comment_count(self, obj):
        return Comment.objects.filter_by_instance(obj).count()

    def get_user_pic(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        
        return image
    

