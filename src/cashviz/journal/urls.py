from django.urls import path

from cashviz.journal.ajax import journal_details
from cashviz.journal.views import JournalEntryList

urlpatterns = [
    path(
        "ajax/journal/details/<int:payment_id>",
        journal_details,
        name="ajax_load_payment_details",
    ),
    path("journal/list/", JournalEntryList.as_view(), name="journal_list"),
]
