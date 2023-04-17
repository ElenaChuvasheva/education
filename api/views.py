from rest_framework import viewsets

from api.serializers import EduModuleSerializer
from educational_module.models import EducationalModule


class EduModuleViewSet(viewsets.ModelViewSet):
    queryset = EducationalModule.objects.all()
    serializer_class = EduModuleSerializer
