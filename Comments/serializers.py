from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )

from .models import Comment
from Accounts.serializers import UserSerializer

User = get_user_model()

def create_comment_serializer(model_type="snippet", slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                "id",
                "parent",
                "content",
                "timestamp",
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            slug = self.slug
            model_qs = ContentType.objects.filter(model=self.model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data
        
        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type, slug, content, main_user,
                parent_obj=parent_obj,
            )
            return comment

    return CommentCreateSerializer

class CommentSerializers(ModelSerializer):
    reply_count = SerializerMethodField()
    username = SerializerMethodField(read_only=True)
    user_pic = SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'timestamp',
            'username',
            'user_pic'
        ]
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_username(self, obj):
        return obj.user.username

    def get_user_pic(self, obj):
        try:
            image = obj.user.image.url
        except:
            image = None
        
        return image

# class CommentListSerializer(ModelSerializer):
#     url = HyperlinkedIdentityField(
#         view_name='thread')
#     reply_count = SerializerMethodField()
#     class Meta:
#         model = Comment
#         fields = [
#             'url',
#             'id',
#             'content',
#             'reply_count',
#             'timestamp',
#         ]
    
#     def get_reply_count(self, obj):
#         if obj.is_parent:
#             return obj.children().count()
#         return 0

class CommentChildSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
        ]

class CommentDetailSerializer(ModelSerializer):
    username = SerializerMethodField(read_only=True)
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    replies =   SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'username',
            'content',
            'reply_count',
            'replies',
            'timestamp',
            'content_object_url',
        ]
        read_only_fields = [
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
    def get_username(self, obj):
        return obj.user.username
    

