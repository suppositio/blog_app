from django.test import TestCase

from src.apps.authors.models import Author
from src.apps.authors.serializers import AuthorSerializer


class AuthorSerializerTest(TestCase):
    def setUp(self):
        self.author_data = {
            'first_name': 'Taras',
            'last_name': 'Shevchenko',
            'email': 'taras.shevchenko@kobzar.ua',
        }

        self.first_name_max_len = Author._meta.get_field('first_name').max_length
        self.last_name_max_len = Author._meta.get_field('last_name').max_length

    def test_create_from_model(self):
        author = Author.objects.create(**self.author_data)
        serializer = AuthorSerializer(instance=author)
        self.assertEqual(set(serializer.data.keys()), {'id', 'first_name', 'last_name', 'email'})
        for field in ['first_name', 'last_name', 'email']:
            self.assertEqual(serializer.data[field], self.author_data[field])

    def test_validate_success(self):
        serializer = AuthorSerializer(data=self.author_data)
        self.assertTrue(serializer.is_valid())

    def test_validate_fail_first_name_missing(self):
        author_data_invalid = self.author_data.copy()
        del author_data_invalid['first_name']
        serializer = AuthorSerializer(data=author_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)

    def test_validate_fail_first_name_blank(self):
        author_data_invalid = self.author_data.copy()
        author_data_invalid['first_name'] = ''
        serializer = AuthorSerializer(data=author_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)

    def test_validate_fail_first_name_too_long(self):
        author_data_invalid = self.author_data.copy()
        too_long_first_name = 'A' * (self.first_name_max_len + 1)
        author_data_invalid['first_name'] = too_long_first_name
        serializer = AuthorSerializer(data=author_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)

    def test_validate_fail_last_name_missing(self):
        author_data_invalid = self.author_data.copy()
        del author_data_invalid['last_name']
        serializer = AuthorSerializer(data=author_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('last_name', serializer.errors)

    def test_validate_fail_last_name_blank(self):
        author_data_invalid = self.author_data.copy()
        author_data_invalid['last_name'] = ''
        serializer = AuthorSerializer(data=author_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('last_name', serializer.errors)

    def test_validate_fail_last_name_too_long(self):
        author_data_invalid = self.author_data.copy()
        too_long_last_name = 'A' * (self.first_name_max_len + 1)
        author_data_invalid['last_name'] = too_long_last_name
        serializer = AuthorSerializer(data=author_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('last_name', serializer.errors) 

    def test_validate_fail_email_missing(self):
        author_data_invalid = self.author_data.copy()
        del author_data_invalid['email']
        serializer = AuthorSerializer(data=author_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_validate_fail_email_invalid(self):
        author_data_invalid = self.author_data.copy()
        author_data_invalid['email'] = 'invalid-email'
        serializer = AuthorSerializer(data=author_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_validate_fail_email_not_unique(self):
        Author.objects.create(**self.author_data)
        serializer = AuthorSerializer(data=self.author_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
