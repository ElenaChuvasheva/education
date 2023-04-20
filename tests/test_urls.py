from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from educational_module.models import EducationalModule


class URLTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_unexisting = '/unexisting/'

    def test_list_url_exists(self):
        '''URL /api/modules/ существует'''
        list_url = reverse('api:module-list')
        self.assertEqual(list_url, '/api/modules/')

    def test_detail_url_exists(self):
        '''URL /api/modules/<int:pk>/ существует'''
        detail_url = reverse('api:module-detail', kwargs={'pk': 1})
        self.assertEqual(detail_url, '/api/modules/1/')

    def test_get_unexisting(self):
        '''Запрос к несуществующей странице вернёт ошибку 404'''
        response = self.client.get(URLTest.url_unexisting)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

