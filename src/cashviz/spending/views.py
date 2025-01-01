from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cashviz.helpers.date import month_list_of_year, month_list_since, years_since
from cashviz.models.category import Category
from cashviz.settings import HELL_START_DATE
from cashviz.spending.helper import (
    get_result_amount_monthly,
    get_single_month_by_target,
    get_yearly_spending,
    get_yearly_spending_result,
)


def spending_monhtly_report(
    request: HttpRequest,
    year: int = date.today().year,
    month: int = date.today().month,
    remove_categories: str = "",
) -> HttpResponse:
    remove = remove_categories.split(",")
    if "" in remove:
        remove.remove("")
    spending = get_single_month_by_target(year=year, month=month, ignore=remove)
    for spend in spending:  # pylint: disable=consider-using-dict-items
        for cat in remove:
            if cat != "":
                del spending[spend][cat]
    results = get_result_amount_monthly(spending)
    payment_categories = [
        dx.name
        for dx in list(Category.objects.all())  # pylint: disable=no-member
        if dx.name not in remove
    ]
    payment_categories.append("total")

    return render(
        request,
        "spending/monthly.html",
        {
            "month_names": [dx.name for dx in month_list_of_year(year)],
            "month": f"{month}.{year}",
            "months": [
                f"{dx.month}.{dx.year}" for dx in month_list_since(HELL_START_DATE)
            ],
            "spendings": spending,
            "payment_categories": payment_categories,
            "result": results,
            "removed": remove,
        },
    )


def spending_yearly_report(
    request: HttpRequest, year: int = date.today().year, remove_categories: str = ""
) -> HttpResponse:
    # noinspection PyArgumentList
    remove = remove_categories.split(",")
    if "" in remove:
        remove.remove("")
    spendings = get_yearly_spending(year, remove)
    results = get_yearly_spending_result(spendings)

    return render(
        request,
        "spending/yearly.html",
        {
            "spendings": spendings,
            "month_names": [dx.name for dx in month_list_of_year(year)],
            "year": year,
            "years": years_since(HELL_START_DATE),
            "result": results,
            "removed": remove,
        },
    )
