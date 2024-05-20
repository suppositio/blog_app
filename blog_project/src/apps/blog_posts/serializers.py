from rest_framework import serializers

from src.apps.blog_posts.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'content',
            'author',
            'categories',
            'created',
            'edited',           
        ]
