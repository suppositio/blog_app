from django.core.exceptions import ValidationError
from django.test import TestCase

from src.apps.authors.models import Author


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author_data = {
            'first_name': 'Taras',
            'last_name': 'Shevchenko',
            'email': 'taras.shevchenko@kobzar.ua',
        }

    def test_str(self):
        author = Author.objects.create(**self.author_data)
        self.assertEqual(
            str(author),
            " ".join((self.author_data['first_name'], self.author_data['last_name']))
        )



