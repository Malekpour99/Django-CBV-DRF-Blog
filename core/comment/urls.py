from django.urls import path

from . import views

app_name = "comment"

urlpatterns = [
    path(
        "post/<slug:slug>/", views.CommentCreateView.as_view(), name="create-comment"
    ),
]
