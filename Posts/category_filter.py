from .models import Post
from .serializers import PostSerializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_filter(request, *args, **kwargs):
    meme = Post.objects.filter(content="#meme_tags")[0:1]    
    game = Post.objects.filter(content="#games_tags")[0:1]
    awesome = Post.objects.filter(content="#awesome_tags")[0:1]
    great = Post.objects.filter(content="#great_tags")[0:1]
    amazing = Post.objects.filter(content="#amazing_tags")[0:1]
    damn = Post.objects.filter(content="#damn_tags")[0:1]


    game_serializer = PostSerializers(instance=game, context={"request": request}, many=True).data
    meme_serializer = PostSerializers(instance=meme, context={"request": request}, many=True).data
    awesome_serializer = PostSerializers(instance=awesome, context={"request": request}, many=True).data
    great_serializer = PostSerializers(instance=great, context={"request": request}, many=True).data
    amazing_serializer = PostSerializers(instance=amazing, context={"request": request}, many=True).data
    damn_serializer = PostSerializers(instance=damn, context={"request": request}, many=True).data
    return Response({ 
        "meme": meme_serializer,
        "game": game_serializer, 
        "awesome": awesome_serializer,
        "great": great_serializer,
        "amazing": amazing_serializer,
        "damn": damn_serializer
        }, status=200)