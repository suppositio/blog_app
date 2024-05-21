from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.apps.authors.models import Author

class AuthorViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author_data = {
            'first_name': 'Taras',
            'last_name': 'Shevchenko',
            'email': 'taras.shevchenko@kobzar.ua',
        }

        self.author = Author.objects.create(**self.author_data)
        self.list_url = reverse('authors:authors')
        self.detail_url = reverse('authors:author_detail', kwargs={'pk': self.author.pk})

    def test_get_list_non_empty(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_empty(self):
        self.author.delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_post(self):
        self.author.delete()
        response = self.client.post(self.list_url, self.author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)

    def test_get_detail_found(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_not_found(self):
        self.author.delete()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_success(self):
        update_data = self.author_data.copy()
        update_data['last_name'] = 'Schewtschenko'
        response = self.client.put(self.detail_url, update_data, format='json')
        self.author.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in update_data.keys():
            self.assertEqual(getattr(self.author, field), update_data[field])

    def test_put_not_found(self):
        self.author.delete()
        update_data = self.author_data.copy()
        update_data['last_name'] = 'Schewtschenko'
        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_success(self):
        update_data = {'last_name': 'Schewtschenko'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.author.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.author.last_name, update_data['last_name'])

    def test_patch_not_found(self):
        self.author.delete()        
        update_data = {'last_name': 'Schewtschenko'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_success(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_delete_not_found(self):
        self.author.delete()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    