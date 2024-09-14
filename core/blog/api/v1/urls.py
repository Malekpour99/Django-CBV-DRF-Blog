from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register("posts", views.PostModelViewSet, basename="post")
router.register("categories", views.CategoryModelViewSet, basename="category")
urlpatterns = router.urls
