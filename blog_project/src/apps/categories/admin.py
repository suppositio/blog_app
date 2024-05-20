from django.contrib import admin

from src.apps.categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Category, CategoryAdmin)
