from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register("posts", views.PostModelViewSet, basename="posts")
urlpatterns = router.urls
