from django.test import Client
from django.urls import reverse, resolve

from rest_framework.test import APITestCase

from api import views


class TestUrls(APITestCase):
    def setUp(self):
        self.url = reverse("api_list")
        self.client = Client()

    def test_api_url(self):
        self.assertEquals(resolve(self.url).func.view_class, views.BookList)

    def test_api_view(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
