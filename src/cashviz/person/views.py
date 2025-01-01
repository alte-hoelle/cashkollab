from django.db.models import Q
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from cashviz.models.journal_entry import JournalEntry
from cashviz.models.person import Person
from cashviz.person.filters import PersonFeeFilter, PersonFeeNotLinkedFilter
from cashviz.person.tables import PersonFeeNotLinkedTable, PersonFeeTable


class PersonFeeView(SingleTableMixin, FilterView):
    template_name = "person/person_fee_details_table.html"
    model = Person
    queryset = Person.member_and_supporter.all()
    table_class = PersonFeeTable
    filterset_class = PersonFeeFilter


class PersonFeeNotLinkedView(SingleTableMixin, FilterView):
    template_name = "person/person_fee_not_linked_table.html"
    model = JournalEntry
    queryset = JournalEntry.objects.filter(
        Q(recipient__is_member=False) & Q(recipient__is_supporter=False)
    ).filter(Q(purpose__name="Mitgliedsbeitrag") | Q(purpose__name="Unterstützung"))
    table_class = PersonFeeNotLinkedTable
    filterset_class = PersonFeeNotLinkedFilter
