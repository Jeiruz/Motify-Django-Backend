from .models import FriendRelation, FriendRequestRelation, FollowerRelation, Profile

def friend_list_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    profile_id = request.GET.get('id')
    return FriendRelation.objects.filter(profile=profile_id)[int(offset): int(offset) + int(limit)]

def request_list_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    profile_id = request.GET.get('id')
    return FriendRequestRelation.objects.filter(profile=profile_id)[int(offset): int(offset) + int(limit)]

def follower_list_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    profile_id = request.GET.get('id')
    return FollowerRelation.objects.filter(profile=profile_id)[int(offset): int(offset) + int(limit)]

def profile_following_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    username = request.GET.get('user')
    return Profile.objects.filter(user__following__user__username=username)[int(offset): int(offset) + int(limit)]