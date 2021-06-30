from Profile.models import Profile, FollowerRelation, FriendRequestRelation
from Posts.models import Post, PostLike
from Profile.serializers import PublicProfileSerializer, FriendRequestRelationSerializer
from Posts.serializers import PostSerializers
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from .serializers import FollowerRelationNotificationSerializer, LikeNotifacationSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_search_filter(request, *args, **kwargs):
    query = request.GET.get("query", None)
    limit = request.GET.get("limit", None)
    offset = request.GET.get('offset', None)
    profile = Profile.objects.all()

    if query:
        profile = profile.filter(
                Q(user__username__icontains=query)).distinct()[int(offset): int(limit) + int(offset)]
                
    profile_serializer = PublicProfileSerializer(instance=profile, context={"request": request}, many=True).data

    return Response(profile_serializer, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_filter(request, *args, **kwargs):
    query = request.GET.get("query", None)
    profile = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(
        Q(user__username__icontains=query, parent=None) | 
        Q(content__icontains=query, parent=None)
        ).distinct()
    tags = Post.objects.filter(parent=None, content__icontains=f"#{query}")

        
                
    profile_serializer = PublicProfileSerializer(instance=profile, context={"request": request}, many=True).data[0:6]
    post_serializer = PostSerializers(instance=posts, context={"request": request}, many=True).data[0:6]
    tags_serializer = PostSerializers(instance=tags, context={"request": request}, many=True).data[0:6]

    return Response({"profile": profile_serializer, "posts": post_serializer, "tags": tags_serializer}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification(request, *args, **kwargs):
    user = request.GET.get("user", None)
    follower = FollowerRelation.objects.filter(profile__user__username=user)
    likes = PostLike.objects.filter(post__user__username=user)
    request = FriendRequestRelation.objects.filter(profile__user__username=user)

    likes_serializer = LikeNotifacationSerializer(instance=likes, context={"request": request}, many=True).data[0:10]
    follower_serializer = FollowerRelationNotificationSerializer(instance=follower, context={"request": request}, many=True).data[0:10]
    request_serializer = FriendRequestRelationSerializer(instance=request, context={"request": request}, many=True).data[0:10]

    return Response({  "follower": follower_serializer, "likes": likes_serializer, "request": request_serializer })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def likes_notification(request, *args, **kwargs):
    user = request.GET.get("user", None)
    limit = request.GET.get("limit", None)
    offset = request.GET.get('offset', None)
    likes = PostLike.objects.filter(post__user__username=user)[int(offset): int(limit) + int(offset)]

    likes_serializer = LikeNotifacationSerializer(instance=likes, context={"request": request}, many=True).data

    return Response({ "data": likes_serializer })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def follower_notification(request, *args, **kwargs):
    user = request.GET.get("user", None)
    limit = request.GET.get("limit", None)
    offset = request.GET.get('offset', None)
    follower = FollowerRelation.objects.filter(profile__user__username=user)[int(offset): int(limit) + int(offset)]

    follower_serializer = FollowerRelationNotificationSerializer(instance=follower, context={"request": request}, many=True).data
    
    return Response({  "data": follower_serializer })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def request_notification(request, *args, **kwargs):
    user = request.GET.get("user", None)
    limit = request.GET.get("limit", None)
    offset = request.GET.get('offset', None)
    request = FriendRequestRelation.objects.filter(profile__user__username=user)[int(offset): int(limit) + int(offset)]

    request_serializer = FriendRequestRelationSerializer(instance=request, context={"request": request}, many=True).data[0:10]

    return Response({ "data": request_serializer })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def no_following_yet(request, *args, **kwargs):
    query = request.GET.get("query", None)
    profile = Profile.objects.all()[0:4]
    posts = Post.objects.filter(parent=None)[0:6]

    profile_serializer = PublicProfileSerializer(instance=profile, context={"request": request}, many=True).data
    post_serializer = PostSerializers(instance=posts, context={"request": request}, many=True).data

    return Response({"profile": profile_serializer, "posts": post_serializer}, status=200)