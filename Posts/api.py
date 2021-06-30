from django.db.models import Q
from rest_framework.response import Response
from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Post, PostLike

from .serializers import (
    # PostDetailSerializer,
    PostSerializers,
    PostActionSerializer,
    PostDetailSerializer,
    CommentListSerializers,
    UserLikeSerializer,
    PostCreateSerializer
    )

from rest_framework import status, generics


from .helper_functions import ( 
    user_like_list_filter,
    tags_filter,
    user_filter,
    user_feed_filter,
    post_search_filter,
    liked_post_filter,
    infinite_filter
    )




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_action_view(request, *args, **kwargs):
    """
    id is required.
    This viewsets also requires Token.
    Action options are: like, unlike, share.
    """
    serializer = PostActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Post.objects.filter(id=post_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = PostSerializers(obj, context={ "request": request})
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = PostSerializers(obj, context={ "request": request})
            return Response(serializer.data, status=200)
        elif action == "share":
            new_post = Post.objects.create(
                user=request.user, 
                parent=obj,
                content=content,
                )
            serializer = PostSerializers(new_post, context={ "request": request})
            return Response(serializer.data, status=201)
    return Response({}, status=200)

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

class CommentListAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentListSerializers
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class UserLikeListAPIView(ListAPIView): 
    serializer_class = UserLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = user_like_list_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response({
            "likes": serializer.data
        })



        
class UserPostAPIView(ListAPIView):
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = user_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response({
            "posts": serializer.data
        })



class UserFeedAPIView(ListAPIView):
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = user_feed_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response({
            "posts": serializer.data
        })


class PostFilterAPIView(ListAPIView): 
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = post_search_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response({
            "posts": serializer.data,
        })

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_delete_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this post"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Post removed"}, status=200)

class LikedPostAPIView(ListAPIView): 
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = liked_post_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response({
            "posts": serializer.data,
        })

class AnonymousPostAPIView(ListAPIView): 
    serializer_class = PostSerializers
    permission_classes = [AllowAny]
    def get_queryset(self):
        qs = infinite_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response(serializer.data)

class ForYouPostAPIView(ListAPIView): 
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = infinite_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response(serializer.data)


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]


class TagsFilterAPIView(ListAPIView): 
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = tags_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={ "request": request})
        return Response({
            "posts": serializer.data,
        })