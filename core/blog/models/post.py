import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .base import BaseModel
from .category import Category


class Post(BaseModel):
    image = models.ImageField(upload_to="blog/", default="default/default-post.png")
    author = models.ForeignKey("accounts.profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name="posts"
    )
    counted_views = models.IntegerField(default=0)
    published_status = models.BooleanField(blank=True, null=True)
    published_at = models.DateTimeField()

    def __str__(self):
        return f" {self.title} - {self.id}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        providing a URL link for previewing posts from admin panel
        """
        return reverse("blog:admin-post-detail", kwargs={"slug": self.slug})

    def get_relative_api_url(self):
        """
        Providing a relative URL path for API response results
        """
        return self.get_absolute_url()

    def get_content_snippet(self):
        """
        providing a snippet for blog post content
        """
        return self.content[0:40] + " ..."
