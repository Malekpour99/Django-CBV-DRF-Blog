from django.urls import path, include

from . import views

app_name = "comment"

urlpatterns = [
    path("post/<slug:slug>/", views.CommentCreateView.as_view(), name="create-comment"),
    path("api/v1/", include("comment.api.v1.urls")),
]
