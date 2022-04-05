from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_filters.views import FilterView

from .filters import BookFilter
from .forms import BookForm, ImportForm
from .models import Book
from .utils import get_json, prepare_objects, get_message


class CreateBook(SuccessMessageMixin, generic.CreateView):
    model = Book
    form_class = BookForm
    context_object_name = "book"
    template_name = "books/partials/form-create.html"

    def get_success_message(self, cleaned_data):
        message = f"Książka {self.object.title} została pomyślnie dodana"
        return message


class UpdateBook(SuccessMessageMixin, generic.UpdateView):
    model = Book
    form_class = BookForm
    context_object_name = "book"
    template_name = "books/partials/form-update.html"

    def get_success_message(self, cleaned_data):
        message = f"Książka {self.object.title} została pomyślnie edytowana"
        return message


class DeleteBook(SuccessMessageMixin, generic.DeleteView):
    model = Book
    context_object_name = "book"
    template_name = "books/partials/form-delete.html"

    def get_success_url(self):
        return reverse_lazy("list")

    def get_success_message(self, cleaned_data):
        message = f"Książka {self.object.title} została pomyślnie usunięta"
        return message


class ListBook(FilterView):
    model = Book
    filterset_class = BookFilter
    context_object_name = "books"
    template_name = "books/partials/list-filter.html"
    paginate_by = 50


def check_validation(request):
    field = list(request.GET)[0]
    form = BookForm(request.GET)
    if field in form.errors.as_data():
        button = render_to_string("books/partials/form-button-disabled.html")
    else:
        button = render_to_string("books/partials/form-button.html")
    return HttpResponse(as_crispy_field(form[f"{field}"]) + button)


def import_books(request):
    if request.method == "POST":
        form = ImportForm(request.POST)
        if form.is_valid():
            data = form.clean()
            try:
                json_list = get_json(data)
            except ValidationError as errors:
                for error in errors:
                    messages.error(request, f"{error}")
            else:
                objects = prepare_objects(json_list)
                books = Book.objects.bulk_create(objects, ignore_conflicts=True)
                message = get_message(books)
                messages.success(request, message)
                return render(request, "books/partials/import_detail.html")
    context = {"form": ImportForm()}
    return render(request, "books/partials/form-import.html", context)


def display_cover(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {"book": book}
    return render(request, "books/partials/display-cover.html", context)
