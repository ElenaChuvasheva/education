from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from api.serializers import EduModuleSerializer
from educational_module.models import EducationalModule


@extend_schema_view(
    list=extend_schema(
        operation_id='Список модулей',
        description='Получение списка модулей'),
    create=extend_schema(
        operation_id='Создание модуля',
        description='Создание модуля'),
    retrieve=extend_schema(
        operation_id='Получение модуля',
        description='Получение информации о выбранном модуле'),
    update=extend_schema(
        operation_id='Изменение модуля',
        description='Перезапись всех полей модуля'),
    partial_update=extend_schema(
        operation_id='Частичное изменение модуля',
        description='Перезапись выбранных полей модуля'),
    destroy=extend_schema(
        operation_id='Удаление выбранного модуля',
        description='Удаление выбранного модуля'),
)
class EduModuleViewSet(viewsets.ModelViewSet):
    queryset = EducationalModule.objects.all()
    serializer_class = EduModuleSerializer
