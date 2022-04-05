from django.urls import path

from api.views import BookList

urlpatterns = [
    path("", BookList.as_view(), name="api_list"),
]
