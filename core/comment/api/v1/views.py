from rest_framework import generics

from comment.models import Comment
from .serializers import CommentSerializer


class CommentListCreateViewSet(generics.ListCreateAPIView):
    """
    Retrieving comments and creating a new comment
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(is_deleted=False, approved=True)
