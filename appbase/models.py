from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    picture = models.ImageField(upload_to="profilePictures/", blank=True, null=True, default="default_profile.png")
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.user:
            return f"Profile of {self.user.username}"
        else:
            return "Profile without a user"
