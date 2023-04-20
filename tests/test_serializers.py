from django.test import TestCase

from api.serializers import EduModuleSerializer
from educational_module.models import EducationalModule


class SerializerTests(TestCase):   
    @classmethod 
    def setUpClass(cls):
        super().setUpClass()
        cls.serializer_data_full = {
            'name': 'test serializer_data_full',
            'description': 'test serializer_data_full description'
        }
        cls.serializer_data_short = {
            'name': 'test serializer_data_short'
        }

        cls.module_attrs_full = {
            'name': 'test module_attrs_full',
            'description': 'test module_attrs_full description'
        }
        cls.module_attrs_short = {
            'name': 'test module_attrs_short'
        }

        cls.module_full = EducationalModule.objects.create(
            **cls.module_attrs_full)
        cls.module_short = EducationalModule.objects.create(
            **cls.module_attrs_short)

        cls.serializer_out_full = EduModuleSerializer(
            instance=cls.module_full)
        cls.serializer_out_short = EduModuleSerializer(
            instance=cls.module_short)

    def test_serializer_in_full(self):
        '''Сериализатор на ввод данных принимает имя и описание'''
        serializer = EduModuleSerializer(
            data=SerializerTests.serializer_data_full)
        self.assertTrue(serializer.is_valid())

    def test_serializer_in_short(self):
        '''При вводе данных поле description необязательно'''
        serializer = EduModuleSerializer(
            data=SerializerTests.serializer_data_short)
        self.assertTrue(serializer.is_valid())

    def test_serializer_out_full(self):
        '''В выводе присутствуют все необходимые поля'''
        data = SerializerTests.serializer_out_full.data
        self.assertCountEqual(data.keys(), ['pk', 'name', 'description'])

    def test_serializer_out_short(self):
        '''В выводе модели без описания присутствуют все необходимые поля'''
        data = SerializerTests.serializer_out_short.data
        self.assertCountEqual(data.keys(), ['pk', 'name', 'description'])

    def test_serializer_full_name_content(self):
        '''Поле name при выводе данных имеет правильное содержание'''
        data = self.serializer_out_full.data
        self.assertEqual(data['name'], self.module_attrs_full['name'])
    
    def test_serializer_full_description_content(self):
        '''Поле description при выводе данных имеет правильное содержание'''
        data = self.serializer_out_full.data
        self.assertEqual(data['description'], self.module_attrs_full['description'])

    def test_serializer_short_name_content(self):
        '''Поле name в объекте без описания при выводе отображается правильно'''
        data = self.serializer_out_short.data
        self.assertEqual(data['name'], self.module_attrs_short['name'])

    def test_serializer_short_description_content(self):
        '''Поле description в объекте без описания при выводе имеет значение None'''
        data = self.serializer_out_short.data
        self.assertIsNone(data['description'])
