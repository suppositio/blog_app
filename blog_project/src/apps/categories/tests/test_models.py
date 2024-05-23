from django.core.exceptions import ValidationError
from django.test import TestCase

from src.apps.categories.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category_data = {
            'name': 'life',
        }

    def test_str(self):
        category = Category.objects.create(**self.category_data)
        self.assertEqual(
            str(category),
            self.category_data['name'],
        )



