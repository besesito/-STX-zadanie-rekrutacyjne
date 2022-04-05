from django.test import SimpleTestCase
from django.urls import resolve, reverse

from books import views


class TestUrls(SimpleTestCase):
    def test_create_url_resolves(self):
        url = reverse("create")
        self.assertEquals(resolve(url).func.view_class, views.CreateBook)

    def test_list_url_resolves(self):
        url = reverse("list")
        self.assertEquals(resolve(url).func.view_class, views.ListBook)

    def test_update_url_resolves(self):
        url = reverse("update", args=["pk"])
        self.assertEquals(resolve(url).func.view_class, views.UpdateBook)

    def test_delete_url_resolves(self):
        url = reverse("delete", args=["pk"])
        self.assertEquals(resolve(url).func.view_class, views.DeleteBook)

    def test_display_cover_url_resolves(self):
        url = reverse("display_cover", args=["pk"])
        self.assertEquals(resolve(url).func, views.display_cover)

    def test_check_validation_url_resolves(self):
        url = reverse("check_validation")
        self.assertEquals(resolve(url).func, views.check_validation)

    def test_import_books_url_resolves(self):
        url = reverse("import_books")
        self.assertEquals(resolve(url).func, views.import_books)
