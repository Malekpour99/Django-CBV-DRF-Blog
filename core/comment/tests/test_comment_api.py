import pytest

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from comment.models import Comment
from accounts.models import Profile
from blog.models import Post


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_user():
    return get_user_model().objects.create_user(
        email="user@test.com", password="commonPassword", is_verified=True
    )


@pytest.fixture
def common_profile(common_user):
    return Profile.objects.get_or_create(user=common_user)[0]


@pytest.fixture
def common_post(common_profile):
    return Post.objects.create(
        title="Test Post",
        content="This is a test post",
        author=common_profile,
        published_at=timezone.now(),
        published_status=True,
    )


@pytest.fixture
def common_comment(common_post, common_profile):
    return Comment.objects.create(
        post=common_post,
        commenter=common_profile,
        subject="Test subject",
        message="This is a test comment",
        approved=True,
        is_deleted=False,
    )


@pytest.mark.django_db
class TestCommentAPI:
    """Tests for CommentListCreateViewSet"""

    def test_list_comments(self, api_client, common_comment):
        url = reverse("comment:api-v1:comment-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert response.data[0]["message"] == common_comment.message

    def test_create_comment(self, api_client, common_user, common_post):
        api_client.force_authenticate(user=common_user)
        url = reverse("comment:api-v1:comment-list")
        data = {
            "post": common_post.id,
            "commenter": common_user.profile.id,
            "subject": "New subject",
            "message": "This is a new comment",
            "approved": True,
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 1
        assert Comment.objects.latest("id").message == "This is a new comment"
