from .models import Post
from .models import PostLike
from django.db.models import Q

# These are all the helper functions use to query a specific object of a  model
def infinite_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    return Post.objects.all()[int(offset): int(offset) + int(limit)]

def user_like_list_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    post = request.GET.get('post')
    return PostLike.objects.filter(post=post)[int(offset): int(offset) + int(limit)]


def tags_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    query = request.GET.get('query')
    return Post.objects.filter(content__icontains=f"#{query}")[int(offset): int(offset) + int(limit)]


def user_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    user = request.GET.get('username')
    return Post.objects.filter(user__username=user)[int(offset): int(offset) + int(limit)]


def user_feed_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    user = request.user
    return Post.objects.feed(user)[int(offset): int(offset) + int(limit)]


def post_search_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    query = request.GET.get('query')
    return Post.objects.filter(
        Q(content__icontains=query) |
        Q(user__username__icontains=query) 
    )[int(offset): int(offset) + int(limit)]

def liked_post_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    user = request.GET.get('user')
    return Post.objects.filter(likes__username=user)[int(offset): int(offset) + int(limit)]