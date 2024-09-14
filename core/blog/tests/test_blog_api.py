import pytest

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Profile
from blog.models import Post, Category


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = get_user_model().objects.create_user(
        email="user@test.com", password="commonPassword", is_verified=True
    )
    return user


@pytest.fixture
def common_profile(common_user):
    profile = Profile.objects.get_or_create(user=common_user)[0]
    return profile


@pytest.fixture
def common_post(common_profile):
    return Post.objects.create(
        title="Test Post",
        content="This is a test post",
        author=common_profile,
        published_at=timezone.now(),
        published_status=True,
    )


@pytest.mark.django_db
class TestBlogPostAPI:
    """API tests for blog app posts"""

    def test_list_posts(self, api_client, common_post, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        results = response.data.get("results", [])
        assert len(results) > 0
        assert results[0]["title"] == common_post.title

    def test_create_post(self, api_client, common_user, common_profile):
        api_client.force_authenticate(user=common_user)
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "New Post",
            "content": "Content of the new post",
            "author": common_profile.id,
            "published_at": timezone.now().isoformat(),
            "published_status": True,
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        # there will be only one post since we are not passing common_post to this method
        assert Post.objects.count() == 1
        assert Post.objects.latest("id").title == "New Post"

    def test_update_post(self, api_client, common_post, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("blog:api-v1:post-detail", args=[common_post.id])
        data = {"title": "Updated Post Title"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        common_post.refresh_from_db()
        assert common_post.title == "Updated Post Title"

    def test_delete_post(self, api_client, common_post, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("blog:api-v1:post-detail", args=[common_post.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Post.objects.get(id=common_post.id).is_deleted

