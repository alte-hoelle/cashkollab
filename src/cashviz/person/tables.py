import django_tables2 as tables

from cashviz.models.journal_entry import JournalEntry
from cashviz.models.person import Person
from config import HELL_CONFIG


class PersonFeeTable(tables.Table):
    details_column = tables.TemplateColumn(
        verbose_name="details",
        template_name="person/person_fee_details_table_button.html",
        orderable=False,
    )
    member_fees_open_column = tables.Column(
        accessor="member_fees_open_as_html", verbose_name="member fees open"
    )

    support_open_column = tables.Column(
        accessor="support_open_as_html", verbose_name="support open"
    )

    class Meta:
        orderable = False
        model = Person
        attrs = {"class": "table table-striped table-hover"}
        fields = (
            "anon_names" if HELL_CONFIG.anon_names else "name",
            "member_fees_open_column",
            "support_open_column",
            "details_column",
        )


class PersonFeeNotLinkedTable(tables.Table):
    class Meta:
        orderable = False
        model = JournalEntry
        attrs = {"class": "table table-striped table-hover"}
        fields = (
            "date",
            "recipient",
            "comment",
            "signed",
            "purpose__name",
        )
