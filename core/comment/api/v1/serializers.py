from rest_framework import serializers

from comment.models import Comment
from accounts.models import Profile


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["commenter", "post", "subject", "message"]
