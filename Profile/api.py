from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView

from .models import Profile
from .serializers import (
    PublicProfileSerializer, 
    ProfilePostListSerializers, 
    FriendRequestRelationSerializer, 
    FriendRelationSerializer, 
    FollowingListSerializer,
    )
from .helper_function import friend_list_filter, request_list_filter, follower_list_filter, profile_following_filter
# Follower and Following
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_detail_api_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, status=404)
    profile_obj = qs.first()
    data = request.data or {}
    if request.method == "POST":
        me = request.user
        action = data.get("action")
        if profile_obj.user != me:
            if action == "follow":
                profile_obj.followers.add(me)
            elif action == "unfollow":
                profile_obj.followers.remove(me)
            elif action == "add_friend":
                profile_obj.friends.add(me)
                profile_obj.followers.add(me)
            elif action == "remove_friend":
                profile_obj.friends.remove(me)
                profile_obj.followers.remove(me)
            elif action == "send_request":
                profile_obj.friend_request.add(me)
            elif action == "remove_request":
                profile_obj.friend_request.remove(me)
            else:
                pass
    serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
    return Response(serializer.data, status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def other_user_friend_action(request, id, *args, **kwargs):
    qs = Profile.objects.filter(user__id=request.user.id)
    if not qs.exists():
        return Response({"detail": "User not found"}, status=404)
    profile_obj = qs.first()
    data = request.data or {}
    if request.method == "POST":
        action = data.get("action")
        if profile_obj.user.id != id:
            if action == "add_friend":
                profile_obj.followers.add(id)
                profile_obj.friends.add(id)
                profile_obj.friend_request.remove(id)
            elif action == "remove_friend":
                profile_obj.followers.remove(id)
                profile_obj.friends.remove(id)
            elif action == "remove_request":
                profile_obj.friend_request.remove(id)
            else:
                pass
    serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
    return Response(serializer.data, status=200)


class FanPageListAIPView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePostListSerializers
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

class RequestListAPIView(ListAPIView):
    serializer_class = FriendRequestRelationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = request_list_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)    


class FollowingListAPIView(ListAPIView):
    serializer_class = PublicProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = profile_following_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)    


class FriendListAPIView(ListAPIView):
    serializer_class = FriendRelationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = friend_list_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)       

class FollowerListAPIView(ListAPIView):
    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = follower_list_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data) 


class ProfileUpdateApiView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = PublicProfileSerializer