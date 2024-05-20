from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.name
