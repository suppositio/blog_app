from django.db import models

from src.apps.authors.models import Author
from src.apps.categories.models import Category


class BlogPost(models.Model):
    title = models.CharField(max_length=150, blank=False)
    content = models.TextField(blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    categories = models.ManyToManyField(Category, null=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


