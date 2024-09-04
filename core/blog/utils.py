from django.utils import timezone

from blog.models import Post


class BlogPostHandler:
    @staticmethod
    def fetch_published_posts():
        """
        Fetches and returns all published blog posts, which are
        not deleted and has lower publication date than today's
        date

        Returns:
            QuerySet[Post]: A queryset of published blog posts.
        """
        return Post.objects.filter(
            published_status=True,
            is_deleted=False,
            published_at__lte=timezone.now(),
        ).order_by("-published_at")

    @staticmethod
    def fetch_user_posts(user_id):
        """
        Fetches and returns user's all blog posts, which are
        not deleted

        Returns:
            QuerySet[Post]: A queryset of user's blog posts.
        """
        return Post.objects.filter(
            author__id=user_id,
            is_deleted=False,
        ).order_by("-published_at")
