from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PostSerializer
from .permissions import IsAuthenticatedAuthor
from .paginations import CustomDefaultPagination
from blog.utils import BlogPostHandler


class PostModelViewSet(viewsets.ModelViewSet):
    """
    Retrieving task and creating a task \n
    Retrieving, Updating and Deleting a single task
    """

    permission_classes = [IsAuthenticatedAuthor]
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = CustomDefaultPagination
    filterset_fields = [
        "published_at",
        "author",
    ]
    search_fields = [
        "title",
        "content",
    ]
    ordering_fields = [
        "published_at",
    ]

    def get_queryset(self):
        return BlogPostHandler.fetch_published_posts()
