from django.db import models


class EducationalModule(models.Model):
    name = models.CharField(
        unique=True, verbose_name='Название', max_length=256)
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Образовательный модуль'
        verbose_name_plural = 'Образовательные модули'

    def __str__(self):
        return self.name
