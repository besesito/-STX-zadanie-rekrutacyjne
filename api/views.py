from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .filters import BookApiFilter
from .serializers import BookSerializer
from books.models import Book


class BookPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 500


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookApiFilter
    pagination_class = BookPagination
