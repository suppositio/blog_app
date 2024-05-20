from drf_spectacular.utils import extend_schema
from rest_framework import generics

from src.apps.authors.models import Author
from src.apps.authors.serializers import AuthorSerializer

@extend_schema(tags=['Authors'])
class AuthorListView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema(tags=['Authors'])
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()