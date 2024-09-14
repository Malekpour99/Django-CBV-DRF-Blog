import pytest

from django.test import Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status

from blog.models import Post, Category


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def common_user():
    user = get_user_model().objects.create_user(
        email="user@test.com", password="commonPassword", is_verified=True
    )
    return user


@pytest.fixture
def super_user():
    user = get_user_model().objects.create_superuser(
        email="admin@test.com", password="adminPassword", is_verified=True
    )
    return user


@pytest.fixture
def common_category():
    return Category.objects.create(name="Test Category")


@pytest.fixture
def common_post(common_user, common_category):
    return Post.objects.create(
        title="Test Post",
        content="This is a test post",
        author=common_user.profile,
        category=common_category,
        published_at=timezone.now(),
        published_status=True,
    )


@pytest.mark.django_db
class TestBlogViews:
    """Tests for blog views"""

    def test_post_list_view(self, client, common_post):
        url = reverse("blog:index")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Test Post" in response.content.decode()

    def test_post_detail_view(self, client, common_post):
        url = reverse("blog:post-detail", args=[common_post.slug])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Test Post" in response.content.decode()

    def test_user_post_detail_view(self, client, common_user, common_post):
        client.force_login(user=common_user)
        url = reverse("blog:user-post-detail", args=[common_post.slug])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Test Post" in response.content.decode()

    def test_user_post_delete_view(self, client, common_user, common_post):
        client.force_login(user=common_user)
        url = reverse("blog:user-post-delete", args=[common_post.slug])
        response = client.post(url)
        assert response.status_code == status.HTTP_302_FOUND  # Redirect after delete
        assert Post.objects.get(id=common_post.id).is_deleted

    def test_user_post_edit_view(self, client, common_user, common_post):
        client.force_login(user=common_user)
        url = reverse("blog:user-post-edit", args=[common_post.slug])
        response = client.post(
            url,
            {
                "title": "Updated Post Title",
                "content": "Updated Content",
                "category": common_post.category.id,
                "published_at": timezone.now(),
            },
        )
        assert response.status_code == status.HTTP_302_FOUND  # Redirect after update
        common_post.refresh_from_db()
        assert common_post.title == "Updated Post Title"

    def test_admin_post_detail_view(self, client, super_user, common_post):
        client.force_login(user=super_user)
        url = reverse("blog:admin-post-detail", args=[common_post.slug])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Test Post" in response.content.decode()

    def test_search_view(self, client, common_post):
        url = reverse("blog:search") + "?search=test"
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Test Post" in response.content.decode()

    def test_post_publish_view(self, client, common_user, common_category):
        client.force_login(user=common_user)
        url = reverse("blog:post-publish")
        response = client.post(
            url,
            {
                "title": "New Post",
                "content": "New content",
                "category": common_category.id,
                "published_at": timezone.now(),
            },
        )
        assert (
            response.status_code == status.HTTP_302_FOUND
        )  # Redirect after successful post
        assert Post.objects.filter(title="New Post").exists()

    def test_category_publish_view(self, client, common_user):
        client.force_login(user=common_user)
        url = reverse("blog:category-publish")
        response = client.post(
            url, {"name": "New Category"}, content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert Category.objects.filter(name="New Category".lower()).exists()

    def test_user_posts_list_view(self, client, common_user, common_post):
        client.login(email="user@test.com", password="commonPassword")
        url = reverse("blog:user-posts")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Test Post" in response.content.decode()
