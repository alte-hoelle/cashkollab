from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def journal_details(request: HttpRequest, payment_id: int) -> HttpResponse:
    print(payment_id)
    return render(request, "journal/person_details.html")
