from django.urls import path

from cashviz.costcenter.views import CostCenterChart, CostCenterOverviewView

urlpatterns = [
    path(
        "cost_centers/overview",
        CostCenterOverviewView.as_view(),
        name="cost_centers_overview",
    ),
    path(
        "api/cost_center/chart",
        CostCenterChart.as_view(),
        name="api_cost_center_overview_chart",
    ),
]
