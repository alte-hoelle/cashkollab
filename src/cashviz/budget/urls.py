from django.urls import path

from cashviz.budget.views import (
    BudgetChartView,
    BudgetOverviewChart,
    BudgetOverviewView,
)

urlpatterns = [
    path("budget/overview/", BudgetOverviewView.as_view(), name="budget_overview"),
    path("budget/charts/", BudgetChartView.as_view(), name="budget_charts"),
    path(
        "api/budget/overview/chart",
        BudgetOverviewChart.as_view(),
        name="api_budget_overview_chart",
    ),
]
