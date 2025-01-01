import django_filters as filters

from cashviz.models.journal_entry import JournalEntry

ATTRS = {"class": "table table-responsive table-striped"}


class JournalEntryFilter(filters.FilterSet):
    class Meta:
        model = JournalEntry
        fields = {
            "recipient__name": ["contains"],
            "purpose__name": ["contains"],
            "comment": ["contains"],
        }
