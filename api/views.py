from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import EduModuleSerializer
from educational_module.models import EducationalModule


class EduModuleViewSet(viewsets.ModelViewSet):
    queryset = EducationalModule.objects.all()
    serializer_class = EduModuleSerializer
