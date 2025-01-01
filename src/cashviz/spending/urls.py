from django.urls import path

from cashviz.spending.views import spending_monhtly_report, spending_yearly_report

urlpatterns = [
    path("spending/yearly/", spending_yearly_report, name="spending_yearly"),
    path(
        "spending/yearly/<str:remove_categories>",
        spending_yearly_report,
        name="spending_yearly",
    ),
    path("spending/yearly/<int:year>/", spending_yearly_report, name="spending_yearly"),
    path(
        "spending/yearly/<int:year>/<str:remove_categories>",
        spending_yearly_report,
        name="spending_yearly",
    ),
    path("spending/monthly/", spending_monhtly_report, name="spending_monthly"),
    path(
        "spending/monthly/<int:year>/<int:month>/",
        spending_monhtly_report,
        name="spending_monthly",
    ),
    path(
        "spending/monthly/<int:year>/<int:month>/<str:remove_categories>",
        spending_monhtly_report,
        name="spending_monthly",
    ),
]
