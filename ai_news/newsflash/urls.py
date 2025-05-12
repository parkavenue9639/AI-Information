from rest_framework import routers
from .views import NewsFlashViewSet

router = routers.DefaultRouter()
router.register(r'newsflash', NewsFlashViewSet)

urlpatterns = router.urls
