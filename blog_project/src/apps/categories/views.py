from drf_spectacular.utils import extend_schema
from rest_framework import generics

from src.apps.categories.models import Category
from src.apps.categories.serializers import CategorySerializer


@extend_schema(tags=['Categories'])
class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


@extend_schema(tags=['Categories'])
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
