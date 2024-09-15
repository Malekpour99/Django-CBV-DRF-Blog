import pytest

from django.test import Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from blog.models import Post
from comment.models import Comment
from accounts.models import Profile


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def common_user(db):
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
        slug="test-post",
        published_at=timezone.now(),
        published_status=True,
    )


@pytest.mark.django_db
class TestCommentViews:
    """Tests for CommentCreateView"""

    def test_create_comment_view_get(self, client, common_user, common_post):
        """Test that the comment form is displayed for authenticated users"""
        client.force_login(user=common_user)
        url = reverse("blog:post-detail", kwargs={"slug": common_post.slug})
        response = client.get(url)

        assert response.status_code == 200
        assert "comment form" in response.content.decode().lower()

    def test_create_comment_success(self, client, common_user, common_post):
        """Test submitting a valid comment as an authenticated user"""
        client.force_login(user=common_user)
        url = reverse("comment:create-comment", kwargs={"slug": common_post.slug})
        post_data = {
            "subject": "Test Comment Subject",
            "message": "This is a test comment message",
        }
        response = client.post(url, post_data)

        # Verify the redirect after successful comment submission
        assert response.status_code == 302
        assert response.url == reverse(
            "blog:post-detail", kwargs={"slug": common_post.slug}
        )

        # Verify the comment was saved
        assert Comment.objects.count() == 1
        new_comment = Comment.objects.latest("id")
        assert new_comment.subject == "Test Comment Subject"
        assert new_comment.message == "This is a test comment message"
        assert new_comment.commenter == common_user.profile
        assert new_comment.post == common_post

        # Verify the success message
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1

    def test_create_comment_unauthenticated_user(self, client, common_post):
        """Test that an unauthenticated user cannot submit a comment"""
        url = reverse("comment:create-comment", kwargs={"slug": common_post.slug})
        post_data = {
            "subject": "Test Comment Subject",
            "message": "This is a test comment message.",
        }
        response = client.post(url, post_data)

        # Verify the unauthenticated user is redirected to the login page
        assert response.status_code == 302
        assert reverse("accounts:login") in response.url
        assert Comment.objects.count() == 0  # No comment should be created
