from django.core.cache import cache
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out


@receiver(user_logged_in)
def clear_cache_on_login(sender, request, user, **kwargs):
    # clearing all cached data
    cache.clear()

    # Or clear specific cache keys
    # cache.delete("cache_key")


@receiver(user_logged_out)
def clear_cache_on_logout(sender, request, user, **kwargs):
    # clearing all cached data
    cache.clear()

    # Or clear specific cache keys
    # cache.delete("cache_key")
