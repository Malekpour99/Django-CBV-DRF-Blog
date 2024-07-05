from typing import Any

from django.utils import timezone
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView

from blog.models import Post


class PostListView(ListView):
    """
    Showing a list of published posts
    """

    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        posts = (
            Post.objects.select_related("author")
            .filter(published_status=True, published_at__lte=timezone.now())
            .order_by("-published_at")
        )
        if self.kwargs.get("cat_slug"):
            posts = posts.filter(category__slug=self.kwargs["cat_slug"])
        return posts


class PostDetailView(DetailView):
    """
    Showing details of a published post
    """

    model = Post
    template_name = "blog/post.html"
