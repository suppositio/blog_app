from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.apps.categories.models import Category

class CategoryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category_data = {
            'name': 'life',
        }

        self.category = Category.objects.create(**self.category_data)
        self.list_url = reverse('categories:categories')
        self.detail_url = reverse('categories:category_detail', kwargs={'pk': self.category.pk})

    def test_get_list_non_empty(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_empty(self):
        self.category.delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_post(self):
        self.category.delete()
        response = self.client.post(self.list_url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.data['name'], self.category_data['name'])

    def test_get_detail_found(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category_data['name'])      

    def test_get_detail_not_found(self):
        self.category.delete()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_success(self):
        update_data = self.category_data.copy()
        update_data['name'] = 'lifestyle'
        response = self.client.put(self.detail_url, update_data, format='json')
        self.category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_put_not_found(self):
        self.category.delete()
        update_data = self.category_data.copy()
        update_data['name'] = 'lifestyle'
        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_success(self):
        update_data = {'name': 'lifestyle'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_patch_not_found(self):
        self.category.delete()        
        update_data = {'name': 'lifestyle'}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_success(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_delete_not_found(self):
        self.category.delete()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    