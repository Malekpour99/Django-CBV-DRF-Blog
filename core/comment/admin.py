from django.contrib import admin

from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    empty_value_display = "-None-"
    list_display = ("commenter", "subject", "approved", "created_at", "is_deleted")
    list_filter = ("created_at", "commenter", "post", "is_deleted")
    search_fields = ["subject", "message", "commenter"]
