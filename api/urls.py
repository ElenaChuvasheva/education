from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import EduModuleViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'modules', EduModuleViewSet, basename='module')

urlpatterns = [
    path('', include(router.urls))
]
