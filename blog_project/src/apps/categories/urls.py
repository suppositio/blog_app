from django.urls import path

from src.apps.categories import views

app_name = "categories"
urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
]