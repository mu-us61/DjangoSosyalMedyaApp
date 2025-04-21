from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    picture = models.ImageField(upload_to="profilePictures/", blank=True, null=True, default="default_profile.png")
    location = models.CharField(max_length=100, blank=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="followed_by", blank=True)
    following = models.ManyToManyField("self", symmetrical=False, related_name="follows", blank=True)

    def __str__(self):
        if self.user:
            return f"Profile of {self.user.username}"
        else:
            return "Profile without a user"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="post_images/")
    caption = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(to=User, related_name="liked_posts", blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s post"
