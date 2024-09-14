import random
from faker import Faker

from django.utils import timezone
from django.core.management.base import BaseCommand

from accounts.models import User, Profile
from blog.models import Post, Category


class Command(BaseCommand):
    help = "Inserting dummy blog posts into the database"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        # creating a fake user and profile
        user = User.objects.create_user(email=self.fake.email(), password="fake@test")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.bio = self.fake.paragraph(nb_sentences=3)
        profile.save()

        # list of some random meaningful categories
        category_names = [
            "technology",
            "health",
            "travel",
            "education",
            "business",
            "lifestyle",
            "entertainment",
            "food",
            "sports",
            "fashion",
        ]

        # Ensure categories exist, or create them
        for category_name in category_names:
            Category.objects.get_or_create(name=category_name)

        categories = Category.objects.all()
        
        # providing a list of default images for blog posts
        default_images = [f"default/default-post-{i}.png" for i in range(1, 11)]

        for _ in range(50):
            Post.objects.create(
                author=profile,
                image=random.choice(default_images),
                title=self.fake.sentence(nb_words=10),
                category=random.choice(categories),
                content=self.fake.paragraph(nb_sentences=10),
                published_status=random.choice([True, False, None]),
                published_at=timezone.now(),
            )
