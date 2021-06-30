from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Q
# from django.contrib.auth.models import User
from Comments.models import Comment
import random
import string
from django.conf import settings


User = settings.AUTH_USER_MODEL

def random_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(35))

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class FeedQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True)
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user) 
        ).distinct().order_by("-timestamp")

class FeedManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return FeedQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

    def active(self, *args, **kwargs):
        return super(FeedManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)



class Post(models.Model):
    user        = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name="post")
    slug = models.CharField(max_length=35, unique=True, default=random_slug)
    parent      = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked", blank=True, through=PostLike)
    content     = models.TextField(max_length=5000, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_location, 
                            blank=True, 
                            width_field="width_field", 
                            height_field="height_field",
                            null=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)


    objects = FeedManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "{}".format(self.pk)

    @property
    def is_share(self):
        return self.parent != None  

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs
    
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
