from django.db.models import Q
from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from .helper_functions import comment_list_filter, is_there_more_comments, comment_reply_filter, is_there_more_replies
from rest_framework.decorators import api_view, permission_classes
 
from Comments.models import Comment




from .serializers import (
    CommentDetailSerializer,
    create_comment_serializer,
    CommentSerializers
    )


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
                model_type=model_type, 
                slug=slug, 
                parent_id=parent_id,
                user=self.request.user
                )


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CommentListAPIView(ListAPIView): 
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = comment_list_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response({
            "comments": serializer.data,
            "has_more": is_there_more_comments(request)
        })


class CommentReplyListAPIView(ListAPIView): 
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = comment_reply_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response({
            "replies": serializer.data,
            "has_more": is_there_more_replies(request)
        })
    

