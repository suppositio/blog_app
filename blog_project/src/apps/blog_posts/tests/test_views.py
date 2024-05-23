from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.apps.authors.models import Author
from src.apps.blog_posts.models import BlogPost
from src.apps.categories.models import Category

class BlogPostViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author_data = {
            'first_name': 'Taras',
            'last_name': 'Shevchenko',
            'email': 'taras.shevchenko@kobzar.ua',
        }

        self.category_data = {
            'name': 'life',
        }

        self.author = Author.objects.create(**self.author_data)
        self.category = Category.objects.create(**self.category_data)

        self.blog_post_data = {
            'title': 'Katerina',
            'content': 'O lovely maidens, fall in love,\nBut not with Muscovites,',
            'author': self.author.id,
            'categories': [self.category.id]
        }

        self.content_update = '\nFor Muscovites are foreign folk,\nThey do not treat you right.'

        self.blog_post = BlogPost.objects.create(
            title=self.blog_post_data['title'],
            content=self.blog_post_data['content'],
            author=self.author,
        )
        self.blog_post.categories.set([self.category])

        self.list_url = reverse('blog_posts:blog_posts')
        self.detail_url = reverse('blog_posts:blog_post_detail', kwargs={'pk': self.blog_post.pk})

    def test_get_list_non_empty(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_empty(self):
        self.blog_post.delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_post(self):
        self.blog_post.delete()
        response = self.client.post(self.list_url, self.blog_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
        for field in self.blog_post_data.keys():
            self.assertEqual(response.data[field], self.blog_post_data[field])

    def test_get_detail_found(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in self.blog_post_data.keys():
            self.assertEqual(response.data[field], self.blog_post_data[field])        

    def test_get_detail_not_found(self):
        self.blog_post.delete()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_success(self):
        update_data = self.blog_post_data.copy()
        update_data['content'] += self.content_update
        response = self.client.put(self.detail_url, update_data, format='json')
        self.blog_post.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in update_data.keys():
            self.assertEqual(response.data[field], update_data[field])

    def test_put_not_found(self):
        self.blog_post.delete()
        update_data = self.blog_post_data.copy()
        update_data['content'] += self.content_update
        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_success(self):
        update_data = {'content': self.blog_post_data['content'] + self.content_update}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.blog_post.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], update_data['content'])

    def test_patch_not_found(self):
        self.blog_post.delete()        
        update_data = {'content': self.blog_post_data['content'] + self.content_update}
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_success(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPost.objects.count(), 0)

    def test_delete_not_found(self):
        self.author.delete()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    