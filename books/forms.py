from django import forms
from django.urls import reverse_lazy

from .models import Book


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[f"{field}"].widget.attrs.update(
                {
                    "hx-get": reverse_lazy("check_validation"),
                    "hx-trigger": "keyup changed delay:600",
                    "hx-target": f"#form_form #div_id_{field}",
                }
            )

    published_date = forms.DateField(
        help_text="Wprowadź datę w formacie RRRR-MM-DD",
        required=False,
        label="Data publikacji",
    )

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
        ]


class ImportForm(forms.Form):
    # Returns results where the text following this keyword is found in the title
    intitle = forms.CharField(max_length=255, label="Tytuł", required=False)

    # Returns results where the text following this keyword is found in the author
    inauthor = forms.CharField(max_length=255, label="Autor", required=False)

    # Returns results where the text following this keyword is found in the publisher
    inpublisher = forms.CharField(max_length=255, label="Wydawca", required=False)

    # Returns results where the text following this keyword is listed in the category list of the volume
    subject = forms.CharField(max_length=255, label="Słowo kluczowe", required=False)

    # Returns results where the text following this keyword is the ISBN number
    isbn = forms.CharField(max_length=255, label="Numer ISBN", required=False)

    # Returns results where the text following this keyword is the Library of Congress Control Number
    lccn = forms.CharField(max_length=255, label="Numer LCCN", required=False)

    # Returns results where the text following this keyword is the Online Computer Library Center number
    oclc = forms.CharField(max_length=255, label="Numer OCLC", required=False)
