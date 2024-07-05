from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path("author/<str:author_username>", views.PostListView.as_view(), name="author"),
    path("category/<slug:cat_slug>", views.PostListView.as_view(), name="category"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
]
