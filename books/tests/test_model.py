from unittest import TestCase

from django.core import exceptions
from django.db import IntegrityError

from books.models import Book


class TestModel(TestCase):
    def setUp(self):
        self.book = Book(
            title="Test Book",
            page_count=394,
            author="Test Author",
            published_date="2022-01-01",
            language="pl",
            cover_url="https://img.com",
        )

    def test_book_create(self):
        self.book.save()
        self.assertIsNotNone(self.book.id)

    def test_book_update(self):
        self.book.save()
        new_date = "2022-01-30"
        self.book.published_date = new_date
        self.book.save()
        self.assertEqual(self.book.published_date, new_date)

    def test_book_delete(self):
        self.book.save()
        self.assertIsNotNone(self.book.id)
        self.book.delete()
        self.assertIsNone(self.book.id)

    def test_validate_date_format(self):
        self.book.published_date = "2011-10"
        self.assertRaises(exceptions.ValidationError, self.book.save)

    #
    def test_validate_isbn_unique(self):
        isbn = 1234512345123
        self.book.isbn = isbn
        self.book.save()
        self.other_book = Book(title="Test Book 2", isbn=isbn)
        self.assertRaises(IntegrityError, self.other_book.save)
