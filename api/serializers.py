from rest_framework import serializers

from educational_module.models import EducationalModule


class EduModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalModule
        fields = ('pk', 'name', 'description')
