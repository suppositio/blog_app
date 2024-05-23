from django.test import TestCase

from src.apps.authors.models import Author
from src.apps.blog_posts.models import BlogPost
from src.apps.categories.models import Category
from src.apps.blog_posts.serializers import BlogPostSerializer


class BlogPostSerializerTest(TestCase):
    def setUp(self):
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
            'content': '''
                O lovely maidens, fall in love,
                But not with Muscovites
            ''',
            'author': self.author.id,
            'categories': [self.category.id]
        }

        self.title_max_len = BlogPost._meta.get_field('title').max_length

    def test_create_from_model(self):
        blog_post = BlogPost.objects.create(
            title=self.blog_post_data['title'],
            content=self.blog_post_data['content'],
            author=self.author,
        )
        blog_post.categories.set([self.category])
        serializer = BlogPostSerializer(instance=blog_post)
        self.assertEqual(set(serializer.data.keys()),
                            {'id', 'title', 'content', 'author', 'categories', 'created', 'edited'},
                        )
        for field in ['title', 'content']:
            self.assertEqual(serializer.data[field], self.blog_post_data[field])
        self.assertEqual(serializer.data['author'], self.author.id)
        self.assertEqual(set(serializer.data['categories']), {self.category.id})

    def test_validate_success(self):
        serializer = BlogPostSerializer(data=self.blog_post_data)
        self.assertTrue(serializer.is_valid())

    def test_validate_fail_title_missing(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        del blog_post_data_invalid['title']
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_validate_fail_title_blank(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        blog_post_data_invalid['title'] = ''
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_validate_fail_title_too_long(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        too_long_title = 'A' * (self.title_max_len + 1)
        blog_post_data_invalid['title'] = too_long_title
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_validate_fail_content_missing(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        del blog_post_data_invalid['content']
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)

    def test_validate_fail_content_blank(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        blog_post_data_invalid['content'] = ''
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)    

    def test_validate_fail_author_missing(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        del blog_post_data_invalid['author']
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('author', serializer.errors)

    def test_validate_fail_author_nonexistent(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        blog_post_data_invalid['author'] = self.author.id + 1
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('author', serializer.errors)

    def test_validate_fail_categories_missing(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        del blog_post_data_invalid['categories']
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('categories', serializer.errors)

    def test_validate_fail_categories_empty(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        blog_post_data_invalid['categories'] = []
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('categories', serializer.errors)

    def test_validate_fail_categories_nonexistent(self):
        blog_post_data_invalid = self.blog_post_data.copy()
        blog_post_data_invalid['categories'] = [self.category.id + 1]
        serializer = BlogPostSerializer(data=blog_post_data_invalid)
        self.assertFalse(serializer.is_valid())
        self.assertIn('categories', serializer.errors)
