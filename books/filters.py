import django_filters

from books.models import Book


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "isbn",
            "cover_url",
            "language",
            "page_count",
            "published_date",
        ]

    ordering = django_filters.OrderingFilter(
        fields=(
            ("title", "Tytuł"),
            ("author", "Autor"),
            ("isbn", "ISBN"),
            ("cover_url", "Link do zdjęcia"),
            ("language", "Język"),
            ("published_date", "Data wydania"),
            ("page_count", "Ilość stron"),
        ),
        label="Sortuj",
    )

    title = django_filters.CharFilter(label="Tytuł", lookup_expr="icontains")
    author = django_filters.CharFilter(label="Autor", lookup_expr="icontains")
    language = django_filters.CharFilter(label="Język", lookup_expr="icontains")
    published_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"})
    )
