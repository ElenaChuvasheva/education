import json

from django.conf import settings
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from api.serializers import EduModuleSerializer
from educational_module.models import EducationalModule

PAGE_SIZE = settings.REST_FRAMEWORK['PAGE_SIZE']
MODULES_NUMBER = PAGE_SIZE + 2


class ViewTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.test_module_data = {'name': 'Тестовый модуль', 'description': 'Тестовое описание'}
        cls.test_module = EducationalModule.objects.create(**cls.test_module_data)
        
        for i in range(1, MODULES_NUMBER):
            EducationalModule.objects.create(
                name=f'Тестовый модуль {i}',
                description=f'Тестовое описание {i}')

    def test_list_1st_page_len(self):
        '''Проверка количества объектов на первой странице пагинатора'''
        response = self.client.get(reverse('api:module-list'))
        results = response.data['results']
        self.assertEqual(len(results), PAGE_SIZE)

    def test_list_2nd_page_len(self):
        '''Проверка количества объектов на второй странице пагинатора'''
        response = self.client.get(reverse('api:module-list')+'?page=2')
        results = response.data['results']
        self.assertEqual(len(results), MODULES_NUMBER - PAGE_SIZE)

    def test_list_content(self):
        '''На первой странице пагинатора содержатся правильные данные'''
        response = self.client.get(reverse('api:module-list'))
        results = json.loads(response.content)['results']
        serializer = EduModuleSerializer(
            EducationalModule.objects.all()[:PAGE_SIZE], many=True)
        self.assertEqual(results, serializer.data)

    def test_detail_get_content(self):
        '''Метод GET возвращает данные о выбранном модуле'''
        pk = ViewTest.test_module.pk
        response = self.client.get(reverse('api:module-detail',
                                           kwargs={'pk': pk}))
        content = json.loads(response.content)
        self.assertEqual(content, {**ViewTest.test_module_data, 'pk': pk})

    def test_post_full_created(self):
        '''Метод POST создаёт объект в базе с именем и описанием'''
        self.client.post(reverse('api:module-list'),
                                           {'name': 'test post full created',
                                            'description': 'test post full created description'},
                                            format='json')
        self.assertTrue(EducationalModule.objects.filter(name='test post full created').exists())
        EducationalModule.objects.get(name='test post full created').delete()

    def test_post_full_content(self):
        '''Метод POST возвращает имя и описание'''
        data = {'name': 'test post full content',
                'description': 'test post full content description'}
        response = self.client.post(reverse('api:module-list'),
                                           data, format='json')
        content = json.loads(response.content)
        new_object = EducationalModule.objects.get(name='test post full content')
        self.assertEqual(content, {**data, 'pk': new_object.pk})
        new_object.delete()

    def test_post_short_created(self):
        '''Метод POST создаёт объект в базе с именем без описания'''
        self.client.post(reverse('api:module-list'),
                                           {'name': 'test post short created'},
                                            format='json')
        created_object = EducationalModule.objects.filter(name='test post short created') 
        self.assertTrue(created_object.exists())
        created_object.delete()

    def test_post_short_content(self):
        '''Метод POST возвращает имя'''
        data = {'name': 'test post short content'}
        response = self.client.post(reverse('api:module-list'),
                                           data, format='json')
        content = json.loads(response.content)
        new_object = EducationalModule.objects.get(
            name='test post short content')
        self.assertEqual(content,
                         {**data, 'pk': new_object.pk, 'description': None})
        new_object.delete()

    def test_patch_name_db(self):
        '''Метод PATCH меняет имя модуля в базе'''
        self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'name': 'patched name'},
                                            format='json')
        ViewTest.test_module.refresh_from_db()
        self.assertEqual(ViewTest.test_module.name, 'patched name')
        ViewTest.test_module.name = ViewTest.test_module_data['name']
        ViewTest.test_module.save()
    
    def test_patch_name_content(self):
        '''Метод PATCH возвращает правильный контент после изменения имени'''
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'name': 'patched name'},
                                            format='json')
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'patched name')
        ViewTest.test_module.save()

    def test_patch_description_db(self):
        '''Метод PATCH меняет описание модуля в базе'''
        self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'description': 'patched description'},
                                            format='json')
        ViewTest.test_module.refresh_from_db()
        self.assertEqual(ViewTest.test_module.description, 'patched description')
        ViewTest.test_module.description = ViewTest.test_module_data['description']
        ViewTest.test_module.save()

    def test_patch_description_content(self):
        '''Метод PATCH возвращает правильный контент после изменения описания'''
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'description': 'patched description'},
                                            format='json')
        content = json.loads(response.content)
        self.assertEqual(content['description'], 'patched description')
        ViewTest.test_module.save()

    def test_put_db(self):
        '''Метод PUT меняет данные модуля в базе'''
        data ={'name': 'put name', 'description': 'put description'}
        pk = ViewTest.test_module.pk
        self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': pk}),
                                           data, format='json')
        put_object = EducationalModule.objects.filter(pk=pk).values()[0]
        self.assertEqual(put_object, {**data, 'id': pk})
        ViewTest.test_module.save()

    def test_put_content(self):
        '''Метод PUT возвращает правильный контент'''
        data ={'name': 'put name', 'description': 'put description'}
        pk = ViewTest.test_module.pk
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': pk}),
                                           data, format='json')
        content = json.loads(response.content)
        self.assertEqual(content, {**data, 'pk': pk})
        ViewTest.test_module.save()

    def test_post_delete_no_object(self):
        '''Метод DELETE удаляет объект в базе'''
        self.client.delete(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}))
        deleted_object_exists = EducationalModule.objects.filter(pk=ViewTest.test_module.pk).exists()        
        self.assertFalse(deleted_object_exists)
        ViewTest.test_module.save()

    def test_get_list_status(self):
        '''Список модулей доступен'''
        response = self.client.get(reverse('api:module-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_status(self):
        '''Данные отдельного модуля доступны'''
        response = self.client.get(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_full_status(self):
        '''Метод POST с указанием имени и описания модуля вернёт код 201'''
        response = self.client.post(reverse('api:module-list'),
                                           {'name': 'test post full status',
                                            'description': 'test post full status description'},
                                            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        EducationalModule.objects.get(name='test post full status').delete()

    def test_post_short_status(self):
        '''Метод POST с указанием имени модуля вернёт код 201'''
        response = self.client.post(reverse('api:module-list'),
                                           {'name': 'test post short status'},
                                            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        EducationalModule.objects.get(name='test post short status').delete()

    def test_patch_status(self):
        '''Метод PATCH с указанием имени модуля вернёт код 200'''
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'name': 'patched name'},
                                            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ViewTest.test_module.save()

    def test_put_status(self):
        '''Метод PUT вернёт код 200'''
        response = self.client.put(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'name': 'put name',
                                            'description': 'put description'},
                                            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ViewTest.test_module.save()

    def test_delete_status(self):
        '''Метод DELETE вернёт код 204'''
        response = self.client.delete(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        ViewTest.test_module.save()
