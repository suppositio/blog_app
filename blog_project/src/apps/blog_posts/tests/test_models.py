from django.core.exceptions import ValidationError
from django.test import TestCase

from src.apps.authors.models import Author
from src.apps.blog_posts.models import BlogPost


class BlogPostModelTest(TestCase):
    def setUp(self):
        self.author_data = {
            'first_name': 'Taras',
            'last_name': 'Shevchenko',
            'email': 'taras.shevchenko@kobzar.ua',
        }

        self.author = Author.objects.create(**self.author_data)

        self.blog_post_data = {
            'title': 'Katerina',
            'content': '''
                O lovely maidens, fall in love,
                But not with Muscovites
            ''',
            'author': self.author,
        }

    def test_str(self):
        blog_post = BlogPost.objects.create(**self.blog_post_data)
        self.assertEqual(
            str(blog_post),
            self.blog_post_data['title'],
        )