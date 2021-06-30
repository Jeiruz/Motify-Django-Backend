from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from Posts.models import Post
from django.contrib.contenttypes.models import ContentType
import random
import string

User = settings.AUTH_USER_MODEL

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

def random_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(35))

class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class FriendRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class FriendRequestRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=220, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True, through=FollowerRelation)
    friends = models.ManyToManyField(User, related_name="friends", blank=True, through=FriendRelation)
    friend_request = models.ManyToManyField(User, related_name="friend_request", through=FriendRequestRelation)
    slug = models.CharField(max_length=35, unique=True, default=random_slug)
    cover_photo = models.ImageField(upload_to=upload_location, 
                            blank=True, 
                            width_field="width_field", 
                            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    background_image = models.ImageField(upload_to=upload_location, 
                            blank=True, 
                            width_field="width_field", 
                            height_field="height_field")
    background_color = models.TextField(default="#1b1a20", max_length=7)
    color = models.TextField(default="white", max_length=7)
    third_color = models.TextField(default="#1a1a1a", max_length=7)

    @property
    def post(self):
        instance = self
        qs = Post.objects.filter_by_instance(instance)
        return qs
    
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)