import json

from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from educational_module.models import EducationalModule


class ViewTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.test_module_data = {'name': 'test module', 'description': 'test description'}        
        cls.test_module = EducationalModule.objects.create(**cls.test_module_data)

    def test_list_len(self):
        response = self.client.get(reverse('api:module-list'))
        results = json.loads(response.content)['results']
        self.assertEqual(len(results), 1)
    
    def test_list_name(self):
        response = self.client.get(reverse('api:module-list'))
        first_result = json.loads(response.content)['results'][0]
        self.assertEqual(first_result['name'], 'test module')

    def test_list_description(self):
        response = self.client.get(reverse('api:module-list'))
        first_result = json.loads(response.content)['results'][0]
        self.assertEqual(first_result['description'], 'test description')

    def test_detail_get_name(self):
        response = self.client.get(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}))
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'test module')

    def test_detail_get_description(self):
        response = self.client.get(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}))
        content = json.loads(response.content)
        self.assertEqual(content['description'], 'test description')

    def test_post_full_created(self):
        response = self.client.post(reverse('api:module-list'),
                                           {'name': 'test post full created',
                                            'description': 'test post full created description'},
                                            format='json')
        self.assertTrue(EducationalModule.objects.filter(name='test post full created').exists())
        EducationalModule.objects.get(name='test post full created').delete()

    def test_post_full_content(self):
        data = {'name': 'test post full content',
                'description': 'test post full content description'}
        response = self.client.post(reverse('api:module-list'),
                                           data, format='json')
        content = json.loads(response.content)
        new_object = EducationalModule.objects.get(name='test post full content')
        self.assertEqual(content, {**data, 'pk': new_object.pk})
        new_object.delete()

    def test_post_short_created(self):
        response = self.client.post(reverse('api:module-list'),
                                           {'name': 'test post short created'},
                                            format='json')
        created_object = EducationalModule.objects.filter(name='test post short created') 
        self.assertTrue(created_object.exists())
        created_object.delete()

    def test_post_short_content(self):
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
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'name': 'patched name'},
                                            format='json')
        ViewTest.test_module.refresh_from_db()
        self.assertEqual(ViewTest.test_module.name, 'patched name')
        ViewTest.test_module.name = ViewTest.test_module_data['name']
        ViewTest.test_module.save()
    
    def test_patch_name_content(self):
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'name': 'patched name'},
                                            format='json')
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'patched name')
        ViewTest.test_module.save()
    
    def test_patch_description_db(self):
        self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'description': 'patched description'},
                                            format='json')
        ViewTest.test_module.refresh_from_db()
        self.assertEqual(ViewTest.test_module.description, 'patched description')
        ViewTest.test_module.description = ViewTest.test_module_data['description']
        ViewTest.test_module.save()

    def test_patch_description_content(self):
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'description': 'patched description'},
                                            format='json')
        content = json.loads(response.content)
        self.assertEqual(content['description'], 'patched description')
        ViewTest.test_module.save()


    def test_put_db(self):
        data ={'name': 'put name', 'description': 'put description'}
        pk = ViewTest.test_module.pk
        self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': pk}),
                                           data, format='json')
        put_object = EducationalModule.objects.filter(pk=pk).values()[0]
        self.assertEqual(put_object, {**data, 'id': pk})
        ViewTest.test_module.save()
#        self.assertEqual(EducationalModule.objects.all().values(), 100500)

    def test_put_content(self):
        data ={'name': 'put name', 'description': 'put description'}
        pk = ViewTest.test_module.pk
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': pk}),
                                           data, format='json')
        content = json.loads(response.content)
        self.assertEqual(content, {**data, 'pk': pk})
        ViewTest.test_module.save()
#        self.assertEqual(EducationalModule.objects.all().values(), 100500)        

    def test_post_delete_no_object(self):
        response = self.client.delete(reverse('api:module-detail',
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
        '''Запрос POST на /api/modules/ с указанием имени и описания модуля вернёт код 201'''
        response = self.client.post(reverse('api:module-list'),
                                           {'name': 'test post full status',
                                            'description': 'test post full status description'},
                                            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        EducationalModule.objects.get(name='test post full status').delete()

    def test_post_short_status(self):
        '''Запрос POST на /api/modules/ с указанием имени модуля вернёт код 201'''
        response = self.client.post(reverse('api:module-list'),
                                           {'name': 'test post short status'},
                                            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        EducationalModule.objects.get(name='test post short status').delete()

    def test_patch_status(self):
        response = self.client.patch(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'name': 'patched name'},
                                            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ViewTest.test_module.save()

    def test_put_status(self):
        response = self.client.put(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}),
                                           {'name': 'put name',
                                            'description': 'put description'},
                                            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ViewTest.test_module.save()

    def test_delete_status(self):
        response = self.client.delete(reverse('api:module-detail',
                                           kwargs={'pk': ViewTest.test_module.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        ViewTest.test_module.save()
