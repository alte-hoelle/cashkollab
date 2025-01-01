from typing import Any, List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from cashviz.budget.helper import get_chart_data, get_overview_data


class BudgetChartView(View):
    # pylint: disable=no-self-use
    def get(self, request: HttpRequest, *__args, **__kwargs) -> HttpResponse:  # type: ignore[no-untyped-def]
        return render(request, "budget/charts.html")


class BudgetOverviewView(View):
    # pylint: disable=no-self-use
    def get(self, request: HttpRequest, *__args, **__kwargs) -> HttpResponse:  # type: ignore[no-untyped-def]
        return render(request, "budget/overview.html", get_overview_data())


class BudgetOverviewChart(APIView):
    authentication_classes: List[str] = []
    permission_classes: List[str] = []

    # pylint: disable=no-self-use
    def get(self, _request: HttpRequest, _format: Any = None) -> Response:
        return Response(get_chart_data())
