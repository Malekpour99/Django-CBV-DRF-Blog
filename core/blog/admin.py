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
        "is_deleted"
    )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("published_status", "author", "category", "is_deleted")
    search_fields = ["title", "content", "author"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
