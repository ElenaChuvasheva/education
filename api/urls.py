from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import EduModuleViewSet

app_name = 'api'

router = SimpleRouter()
router.register('educational_modules', EduModuleViewSet)

urlpatterns = [
    path('', include(router.urls))
]
