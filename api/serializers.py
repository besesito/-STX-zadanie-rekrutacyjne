from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "published_date",
            "isbn",
            "page_count",
            "cover_url",
            "language",
            "id",
        ]
