from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from cashviz.journal.filters import JournalEntryFilter
from cashviz.journal.tables import JournalEntryTable
from cashviz.models.journal_entry import JournalEntry


class JournalEntryList(SingleTableMixin, FilterView):
    template_name = "journal/journal_list.html"
    model = JournalEntry
    queryset = JournalEntry.objects.all()  # pylint: disable=no-member
    table_class = JournalEntryTable
    filterset_class = JournalEntryFilter
