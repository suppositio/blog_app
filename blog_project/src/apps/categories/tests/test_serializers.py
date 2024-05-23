from django.test import TestCase

from src.apps.categories.models import Category
from src.apps.categories.serializers import CategorySerializer


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category_data = {
            'name': 'life',
        }

        self.name_max_len = Category._meta.get_field('name').max_length

    def test_create_from_model(self):
        category = Category.objects.create(**self.category_data)
        serializer = CategorySerializer(instance=category)
        self.assertEqual(set(serializer.data.keys()), {'id', 'name'})
        self.assertEqual(serializer.data['name'], self.category_data['name'])

    def test_validate_success(self):
        serializer = CategorySerializer(data=self.category_data)
        self.assertTrue(serializer.is_valid())

    def test_validate_fail_name_missing(self):
        category_data_invalid = self.category_data.copy()
        del category_data_invalid['name']
        serializer = CategorySerializer(data=category_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_validate_fail_name_blank(self):
        category_data_invalid = self.category_data.copy()
        category_data_invalid['name'] = ''
        serializer = CategorySerializer(data=category_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_validate_fail_name_too_long(self):
        category_data_invalid = self.category_data.copy()
        too_long_name = 'A' * (self.name_max_len + 1)
        category_data_invalid['name'] = too_long_name
        serializer = CategorySerializer(data=category_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_validate_fail_name_not_unique(self):
        Category.objects.create(**self.category_data)
        serializer = CategorySerializer(data=self.category_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
