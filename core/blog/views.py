from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from blog.models import Post


class PostListView(ListView):
    """
    Showing a list of published posts
    """

    template_name = "blog/index.html"
    queryset = Post.objects.select_related("author").filter(published_status=True)
    context_object_name = "posts"


class PostDetailView(DetailView):
    """
    Showing details of a published post
    """

    model = Post
    template_name = "blog/post.html"
