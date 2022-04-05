from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Book(models.Model):
    class Meta:
        ordering = ["title"]

    title = models.CharField(
        max_length=255,
        verbose_name="tytuł",
    )
    author = models.CharField(max_length=255, blank=True, verbose_name="autor")
    published_date = models.DateField(
        blank=True, null=True, verbose_name="data publikacji"
    )
    isbn = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name="numer ISBN",
        unique=True,
        error_messages={"unique": "Istnieje już książka o takim numerze ISBN"},
        validators=[MinValueValidator(1)],
    )
    page_count = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="liczba stron"
    )
    cover_url = models.URLField(blank=True, null=True, verbose_name="link do zdjęcia")
    language = models.CharField(
        max_length=255, blank=True, verbose_name="język publikacji"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("list")
