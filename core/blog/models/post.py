import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .base import BaseModel
from .category import Category


class Post(BaseModel):
    image = models.ImageField(upload_to="blog/", default="blog/default-post.svg")
    author = models.ForeignKey("accounts.profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="posts"
    )
    counted_views = models.IntegerField(default=0)
    published_status = models.BooleanField(default=False)
    published_at = models.DateTimeField()

    def __str__(self):
        return f" {self.title} - {self.id}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if Post.objects.filter(slug=self.slug).exists():
            self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:single", kwargs={"pid": self.id})
