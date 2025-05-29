from rest_framework.routers import DefaultRouter

from .views import URLShortenerViewSet

router = DefaultRouter()
router.register(r"shorten", URLShortenerViewSet, basename="shorten")

urlpatterns = router.urls
