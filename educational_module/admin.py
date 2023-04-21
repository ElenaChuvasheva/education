from django.contrib import admin

from educational_module.models import EducationalModule


@admin.register(EducationalModule)
class EducationalModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')
    empty_value_display = '-пусто-'
