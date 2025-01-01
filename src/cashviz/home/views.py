from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = "home.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:  # type: ignore[no-untyped-def]
        return render(request, "home.html")
