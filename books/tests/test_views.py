from django.test import TestCase, Client
from django.urls import reverse

from books.models import Book


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_get(self):
        response = self.client.get(reverse("create"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/form-create.html")

    def test_create_post(self):
        data = {"title": "Test Book"}
        response = self.client.post(reverse("create"), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Book.objects.last().title, "Test Book")

    def test_create_no_data_post(self):
        self.client.post(reverse("create"))
        self.assertEquals(Book.objects.count(), 0)

    def test_update_get(self):
        book = Book.objects.create(title="Book To Update")
        response = self.client.get(reverse("update", args=[book.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/form-update.html")

    def test_update_post(self):
        book = Book.objects.create(title="Book To Update")
        data = {"title": "Book Updated"}
        response = self.client.post(reverse("update", args=[book.id]), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Book.objects.last().title, "Book Updated")

    def test_list_get(self):
        response = self.client.get(reverse("list"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/list-filter.html")

    def test_delete_get(self):
        book_to_delete = Book.objects.create(title="Book To Delete")
        response = self.client.get(reverse("delete", args=[book_to_delete.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/form-delete.html")

    def test_delete_delete(self):
        book_to_delete = Book.objects.create(title="Book To Delete")
        self.assertEquals(Book.objects.count(), 1)
        response = self.client.delete(reverse("delete", args=[book_to_delete.id]))
        self.assertEquals(Book.objects.count(), 0)
        self.assertEquals(response.status_code, 302)

    def test_check_validation_get(self):
        data = {"title": "Form to Validate"}
        response = self.client.get(reverse("check_validation"), data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/form-button.html")

        data = {"published_date": "Wrong Format of Date"}
        response = self.client.get(reverse("check_validation"), data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/form-button-disabled.html")

        with self.assertRaises(KeyError):
            data = {"wrong_key": "Form to Validate"}
            self.client.get(reverse("check_validation"), data)

    def test_import_books_get(self):
        response = self.client.get(reverse("import_books"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/form-import.html")

    def test_import_books_post(self):
        response = self.client.post(reverse("import_books"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/import_detail.html")

    def test_display_cover_get(self):
        book = Book.objects.create()
        response = self.client.get(reverse("display_cover", args=[book.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "books/partials/display-cover.html")
