import datetime
import requests
import threading

from django.core.exceptions import ValidationError

from books.models import Book


def get_request(url, json_list: list):
    r = requests.get(url)
    json_list.append(r.json())


def get_json(data: dict):
    q = "q="
    for key, value in data.items():
        if value:
            q += f"{key}:{value}&"
    try:
        json_list = list()
        max_results = 40
        r = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?{q}maxResults={max_results}"
        )
        json_list.append(r.json())

        if r.status_code == 200:
            total_items = r.json()["totalItems"]
            if total_items > 0:
                if total_items <= 40:
                    return json_list
                else:
                    threads = list()

                    for index in range(41, total_items - 1, 40):
                        url = f"https://www.googleapis.com/books/v1/volumes?{q}maxResults={max_results}&startIndex={index}"
                        t = threading.Thread(target=get_request, args=[url, json_list])
                        t.start()
                        threads.append(t)

                    for thread in threads:
                        thread.join()
                    return json_list
            else:
                raise ValidationError("Nie odnaleziono książki spełniającej kryteria")
        else:
            raise ValidationError("Błąd odpowiedzi serwera")
    except requests.RequestException:
        raise ValidationError("Błąd z pobieraniem danych")


def prepare_objects(json_list):
    objects = list()
    for page in json_list:
        try:
            for book in page["items"]:
                title = book["volumeInfo"]["title"]
                try:
                    published_date = book["volumeInfo"]["publishedDate"]
                    published_date += "-01-01"
                    published_date = published_date[:10]
                    try:
                        datetime.datetime.strptime(published_date, "%Y-%m-%d")
                    except ValueError:
                        published_date = None
                except KeyError:
                    published_date = None
                try:
                    authors = ""
                    for author in book["volumeInfo"]["authors"]:
                        authors += author
                except KeyError:
                    authors = ""
                isbn = None
                try:
                    for identifier in book["volumeInfo"]["industryIdentifiers"]:
                        if identifier["type"] == "ISBN_13":
                            isbn = identifier["identifier"]
                except KeyError:
                    isbn = None
                try:
                    page_count = book["volumeInfo"]["pageCount"]
                except KeyError:
                    page_count = None
                try:
                    cover_url = book["volumeInfo"]["imageLinks"]["thumbnail"]
                except KeyError:
                    cover_url = None
                try:
                    language = book["volumeInfo"]["language"]
                except KeyError:
                    language = ""

                if not Book.objects.filter(isbn=isbn):
                    objects.append(
                        Book(
                            title=title,
                            author=authors,
                            published_date=published_date,
                            isbn=isbn,
                            page_count=page_count,
                            language=language,
                            cover_url=cover_url,
                        )
                    )
        except KeyError:
            pass
    return objects


def get_message(books):
    if len(books) > 1:
        return f"{len(books)} x książka została dodana do bazy danych"
    elif len(books) == 0:
        return f"Posiadasz już wyszukane książki w bazie"
    else:
        return f"Książka - {books[0].title} - została dodana do bazy danych"
