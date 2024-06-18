from django.contrib import admin
from blog.models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    empty_value_display = "-None-"
    list_display = (
        "title",
        "published_at",
        "author",
        "category",
        "counted_views",
        "published_status",
        "created_at",
    )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("published_status", "author", "category")
    search_fields = ["title", "content"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
