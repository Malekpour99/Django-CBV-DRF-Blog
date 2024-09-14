from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    path("comments/", views.CommentListCreateViewSet.as_view(), name="comment-list"),
]
