from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from blog.models import Category
from blog.utils import BlogPostHandler
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsAuthenticatedAuthor
from .paginations import CustomDefaultPagination


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


class CategoryModelViewSet(viewsets.ModelViewSet):
    """
    Retrieving category and creating a category \n
    Retrieving, Updating and Deleting a single category
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
