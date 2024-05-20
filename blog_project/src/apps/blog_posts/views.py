from drf_spectacular.utils import extend_schema
from rest_framework import generics

from src.apps.blog_posts.models import BlogPost
from src.apps.blog_posts.serializers import BlogPostSerializer


@extend_schema(tags=['Blog posts'])
class BlogPostListView(generics.ListCreateAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.prefetch_related('author', 'categories')


@extend_schema(tags=['Blog posts'])
class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.prefetch_related('author', 'categories')