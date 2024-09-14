import json
from typing import Any

from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from rest_framework import status

from blog.models import Post, Category
from blog.utils import BlogPostHandler
from comment.models import Comment


class PostListView(ListView):
    """
    Showing a list of published posts
    """

    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 7

    def get_queryset(self) -> QuerySet[Any]:
        posts = BlogPostHandler.fetch_published_posts()
        if self.kwargs.get("cat_slug"):
            posts = posts.filter(category__slug=self.kwargs["cat_slug"])
        if self.kwargs.get("author_username"):
            posts = posts.filter(author__username=self.kwargs["author_username"])
        return posts

    def get_context_data(self, **kwargs):
        is_home = True
        context = super().get_context_data(**kwargs)
        categories = (
            Category.objects.filter(is_deleted=False)
            .order_by("name")
            .annotate(
                published_post_count=Count(
                    "posts",
                    filter=Q(posts__published_status=True, posts__is_deleted=False),
                )
            )
        )

        if self.kwargs.get("cat_slug"):
            category = self.kwargs["cat_slug"]
            page_title = f"Posts in '{category.capitalize()}' category"
            is_home = False
        elif self.kwargs.get("author_username"):
            author = self.kwargs["author_username"]
            page_title = f"Posts by '{author.capitalize()}'"
            is_home = False
        else:
            page_title = "Recent Posts"

        context["page_title"] = page_title
        context["categories"] = categories
        context["selected_category"] = self.kwargs.get("cat_slug")
        context["is_home"] = is_home

        return context


class PostDetailView(DetailView):
    """
    Showing details of a published post
    """

    model = Post
    template_name = "blog/post.html"

    def get_queryset(self) -> QuerySet[Any]:
        return BlogPostHandler.fetch_published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_comments = Comment.objects.filter(
            post__slug=self.kwargs.get("slug"), is_deleted=False, approved=True
        ).select_related("commenter")
        
        context["comments"] = post_comments
        return context


class UserPostDetailView(DetailView):
    """
    Showing details of a user's post
    """

    model = Post
    template_name = "blog/post.html"

    def get_queryset(self) -> QuerySet[Any]:
        return BlogPostHandler.fetch_user_posts(self.request.user.id)


class UserPostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deleting desired post which if it's owned by authenticated user
    """

    template_name = "blog/user_posts.html"

    def get_queryset(self):
        return BlogPostHandler.fetch_user_posts(self.request.user.id)

    def get_success_url(self):
        return reverse_lazy("blog:user-posts")


class UserPostEditView(LoginRequiredMixin, UpdateView):
    """
    Editing desired post which if it's owned by authenticated user
    """

    template_name = "blog/post_edit.html"
    fields = ["image", "title", "content", "category", "published_at"]
    success_url = reverse_lazy("blog:user-posts")

    def get_queryset(self):
        return BlogPostHandler.fetch_user_posts(self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(is_deleted=False).order_by("name")
        context["categories"] = categories

        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        # Set published_status to None, which is considered as the pending status
        post.published_status = None
        post.save()

        return super().form_valid(form)


class AdminPostDetailView(DetailView):
    """
    Showing details of any post to admin users
    """

    model = Post
    template_name = "blog/post.html"

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_superuser:
            return Post.objects.all()


class SearchView(View):
    """
    Searching blog posts
    """

    def get(self, request, *args, **kwargs):
        search_query = self.request.GET.get("search", "")
        posts = BlogPostHandler.fetch_published_posts().filter(
            Q(content__icontains=search_query) | Q(title__icontains=search_query)
        )
        page_title = "Search results for: " + '"' + search_query + '"'
        context = {
            "page_title": page_title,
            "posts": posts,
            "is_home": False,
        }
        return render(request, "blog/index.html", context)


class PostPublishView(LoginRequiredMixin, CreateView):
    """
    Provides a form for users to publish a new post
    """

    template_name = "blog/post_publish.html"
    model = Post
    fields = ["image", "title", "content", "category", "published_at"]
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Post created successfully! It will be published after approval.",
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = "Publish a new Post"
        categories = Category.objects.filter(is_deleted=False).order_by("name")

        context["page_title"] = page_title
        context["categories"] = categories

        return context


class CategoryPublishView(LoginRequiredMixin, View):
    """
    Provides a form for users to create a new category
    """

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            category_name = data.get("name")

            if not category_name:
                return JsonResponse(
                    {"error": "Category name is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if category already exists
            if Category.objects.filter(name=category_name).exists():
                return JsonResponse(
                    {"error": f"'{category_name}' category already exists!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create new category
            category = Category.objects.create(name=category_name)

            return JsonResponse(
                {
                    "success": True,
                    "category_id": category.id,
                    "category_name": category.name,
                }
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserPostsListView(LoginRequiredMixin, ListView):
    """
    Showing a list of user published, pending, rejected and deleted posts.
    """

    template_name = "blog/user_posts.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        posts = BlogPostHandler.fetch_user_posts(self.request.user.id)
        return posts

    def get_context_data(self, **kwargs):
        is_home = False
        context = super().get_context_data(**kwargs)

        context["is_home"] = is_home
        return context
