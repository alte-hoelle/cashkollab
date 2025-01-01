from datetime import date
from typing import Any, List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from cashviz.costcenter.helper import get_expense_per_month
from cashviz.helpers.date import month_list_since
from cashviz.models.purpose import Purpose
from config import HELL_CONFIG

# pylint: disable=unused-argument,no-self-use


class CostCenterOverviewView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:  # type: ignore[no-untyped-def]
        return render(request, "costcenter/overview.html")


class CostCenterChart(APIView):
    authentication_classes: List[str] = []
    permission_classes: List[str] = []

    def get(self, request: HttpRequest, _format: Any = None) -> Response:
        budgets = list(Purpose.objects.all())  # pylint: disable=no-member
        months = month_list_since(date(2021, 5, 1))
        labels = [dt[2] for dt in months]
        chartlabel = [
            x.name for x in budgets if x.name not in HELL_CONFIG.spending.exclude
        ]
        chartdata = [
            get_expense_per_month(x, months)
            for x in budgets
            if x.name not in HELL_CONFIG.spending.exclude
        ]

        return Response(
            {
                "labels": labels,
                "chartLabel": chartlabel,
                "chartdatalist": chartdata,
                "len_graphs": len(chartdata),
            }
        )
