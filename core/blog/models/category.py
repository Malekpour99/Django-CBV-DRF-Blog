import uuid

from django.db import models
from django.utils.text import slugify

from .base import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ensuring names uniqueness for any database
        self.name = self.name.lower().strip()
        if not self.slug:
            self.slug = slugify(self.name)
        if Category.objects.filter(slug=self.slug).exists():
            self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
