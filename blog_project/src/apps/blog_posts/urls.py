from django.urls import path

from src.apps.blog_posts import views

app_name = "blog_posts"
urlpatterns = [
    path('blog_posts/', views.BlogPostListView.as_view(), name='blog_posts'),
    path('blog_posts/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
]