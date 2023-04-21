from django.test import TestCase

from educational_module.models import EducationalModule


class ModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_module = EducationalModule.objects.create(
            name='Тестовый модуль', description='Тестовое описание')
    
    def test_str_method(self):
        '''Метод __str__ работает правильно'''
        self.assertEqual(str(ModelTest.test_module), 'Тестовый модуль')
        
    def test_verboses(self):
        '''Указаны правильные verbose_name'''
        field_verboses = {
            'name': 'Название модуля',
            'description': 'Описание'
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    ModelTest.test_module._meta.get_field(field).verbose_name,
                    expected)
