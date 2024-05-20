from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return " ".join((self.first_name, self.last_name))
