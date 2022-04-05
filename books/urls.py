from django.urls import path

from .views import *

urlpatterns = [
    path("create", CreateBook.as_view(), name="create"),
    path("list", ListBook.as_view(), name="list"),
    path("<str:pk>/update", UpdateBook.as_view(), name="update"),
    path("<str:pk>/delete", DeleteBook.as_view(), name="delete"),
    path("<str:pk>/display_cover", display_cover, name="display_cover"),
    path("check_validation", check_validation, name="check_validation"),
    path("import_books", import_books, name="import_books"),
]
