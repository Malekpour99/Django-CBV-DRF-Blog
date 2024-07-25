from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path("author/<str:author_username>", views.PostListView.as_view(), name="author"),
    path("category/<slug:cat_slug>", views.PostListView.as_view(), name="category"),
    path("posts/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("post-publish/", views.PostPublishView.as_view(), name="post-publish"),
    path("category-publish/", views.CategoryPublishView.as_view(), name="category-publish"),
]
