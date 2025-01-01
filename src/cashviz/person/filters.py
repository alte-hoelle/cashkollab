import django_filters as filters

from cashviz.models.journal_entry import JournalEntry
from cashviz.models.person import Person

ATTRS = {"class": "table table-responsive table-striped"}


class PersonFeeFilter(filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            "name": ["icontains"],
            # "account__iban": ["iexact"],
        }


class PersonFeeNotLinkedFilter(filters.FilterSet):
    class Meta:
        model = JournalEntry
        fields = {
            "recipient__name": ["icontains"],
            "purpose__name": ["iexact"],
        }
