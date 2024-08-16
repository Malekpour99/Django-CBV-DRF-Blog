import uuid

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from .users import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    image = models.ImageField(
        upload_to="accounts/", default="default/default-profile.jpg"
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user.email.split("@")[0]
        if Profile.objects.filter(username=self.username).exists():
            self.username = f"{self.username}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
