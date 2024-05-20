from django.contrib import admin

from src.apps.authors.models import Author


class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']

admin.site.register(Author, AuthorAdmin)
