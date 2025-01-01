from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from cashviz.importer.update_database import update_database


class ImportDatabaseView(TemplateView):
    template_name = "home.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:  # type: ignore[no-untyped-def]
        update_database()
        return render(request, "update_database.html")
