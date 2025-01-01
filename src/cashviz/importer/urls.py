from django.urls import path

from cashviz.importer.views import ImportDatabaseView

urlpatterns = [
    path(
        "update/database",
        ImportDatabaseView.as_view(),
        name="update_database",
    ),
]
