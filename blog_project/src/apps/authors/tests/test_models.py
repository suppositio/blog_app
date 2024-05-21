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

        self.first_name_max_len = Author._meta.get_field('first_name').max_length
        self.last_name_max_len = Author._meta.get_field('last_name').max_length


    def test_create_success(self):
        author = Author.objects.create(**self.author_data)
        for field, value in self.author_data.items():
            self.assertEqual(getattr(author, field), value)
    
    def test_create_fail_first_name_blank(self):
        author_data_invalid = self.author_data.copy()
        author_data_invalid['first_name'] = ''
        with self.assertRaises(ValidationError):
            author = Author(**author_data_invalid)
            author.full_clean()

    def test_create_fail_first_name_too_long(self):
        author_data_invalid = self.author_data.copy()
        too_long_first_name = 'A' * (self.first_name_max_len + 1)
        author_data_invalid['first_name'] = too_long_first_name
        with self.assertRaises(ValidationError):
            author = Author(**author_data_invalid)
            author.full_clean()   

    def test_create_fail_last_name_blank(self):
        author_data_invalid = self.author_data.copy()
        author_data_invalid['last_name'] = ''
        with self.assertRaises(ValidationError):
            author = Author(**author_data_invalid)
            author.full_clean()

    def test_create_fail_last_name_too_long(self):
        author_data_invalid = self.author_data.copy()
        too_long_last_name = 'A' * (self.last_name_max_len + 1)
        author_data_invalid['last_name'] = too_long_last_name
        with self.assertRaises(ValidationError):
            author = Author(**author_data_invalid)
            author.full_clean()  

    def test_create_fail_email_invalid(self):
        author_data_invalid = self.author_data.copy()
        author_data_invalid['email'] = 'invalid-email'
        with self.assertRaises(ValidationError):
            author = Author(**author_data_invalid)
            author.full_clean()

    def test_create_fail_email_not_unique(self):
        Author.objects.create(**self.author_data)
        with self.assertRaises(ValidationError):
            author = Author(**self.author_data)
            author.full_clean()

    def test_str(self):
        author = Author.objects.create(**self.author_data)
        self.assertEqual(
            str(author),
            " ".join((self.author_data['first_name'], self.author_data['last_name']))
        )



