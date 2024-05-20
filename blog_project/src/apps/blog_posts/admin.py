from django.contrib import admin

from src.apps.blog_posts.models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'content',
        'author',
        'categories',
    ] 

admin.site.register(BlogPost, BlogPostAdmin)