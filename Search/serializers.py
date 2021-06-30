from Posts.models import Post, PostLike
from Posts.serializers import UserLikeSerializer
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    Serializer,
    IntegerField,
    CharField,
    PrimaryKeyRelatedField,
    Field,
    ListField
    )
from Profile.models import FollowerRelation
from Comments.models import Comment


class LikeNotifacationSerializer(ModelSerializer):
    model_type = SerializerMethodField(read_only=True)
    user = SerializerMethodField(read_only=True)
    image = SerializerMethodField(read_only=True)
    slug = SerializerMethodField(read_only=True)
    timestamp = SerializerMethodField(read_only=True)

    class Meta:
        model = PostLike
        fields = ["model_type", "timestamp", "user", "image", "slug"]

    def get_model_type(self, obj):
        return "likes"

    def get_user(self, obj):
        return obj.user.username

    def get_image(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        return image
    
    def get_slug(self, obj):
        return obj.post.slug
    
    def get_timestamp(self, obj):
        return obj.date


class CommentSerializers(ModelSerializer):
    username = SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
          'username'
        ]

    def get_username(self, obj):
        return obj.user.username

class CommentNoticationSerializer(ModelSerializer):
    user = SerializerMethodField(read_only=True)
    model_type = SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ["slug", "user", "model_type", "timestamp"]

    def get_user(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)[0:1]
        comments = CommentSerializers(c_qs, many=True).data
        return comments

    def get_model_type(self, obj):
        return "comment"

class FollowerRelationNotificationSerializer(ModelSerializer):
    user = SerializerMethodField(read_only=True)
    model_type = SerializerMethodField(read_only=True)
    image = SerializerMethodField(read_only=True)

    class Meta:
        model = FollowerRelation
        fields = ["user", "model_type", "timestamp", "image"]

    def get_user(self, obj):
        return obj.user.username
    
    def get_model_type(self, obj):
        return "follower"
    
    def get_image(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        return image