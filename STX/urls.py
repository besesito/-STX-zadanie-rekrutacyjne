from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import generic

urlpatterns = [
    path("", generic.TemplateView.as_view(template_name="base.html"), name="home"),
    path("admin/", admin.site.urls),
    path("book/", include("books.urls")),
    path("api/", include("api.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
