from django.db import models

from blog.models import Post
from accounts.models import Profile
from blog.models.base import BaseModel


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="user_comments"
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.commenter.username} - {self.subject}"
