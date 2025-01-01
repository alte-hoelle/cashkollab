import django_tables2 as tables

from cashviz.models.journal_entry import JournalEntry
from config.example_config import HELL_CONFIG


class JournalEntryTable(tables.Table):
    my_attr = {"td": {"class": "text-end"}, "th": {"class": "text-end"}}
    date = tables.DateColumn(format="d M Y")
    # button = tables.TemplateColumn(
    #    verbose_name="show details",
    #    template_name="payment/payment_table_button.html",
    #    orderable=False,
    # )  # orderable not sortable

    tax_formatted_column = tables.Column(
        accessor="taxes_formatted", verbose_name="Tax", attrs=my_attr
    )

    signed_colored_column = tables.Column(
        accessor="signed_colored", verbose_name="Brutto", attrs=my_attr
    )

    signed_netto_colored_column = tables.Column(
        accessor="signed_netto_colored", verbose_name="Netto", attrs=my_attr
    )

    category_name = tables.Column(accessor="category.name", verbose_name="Category")

    class Meta:
        model = JournalEntry
        attrs = {
            "class": "table table-striped table-hover",
        }
        fields = (
            "date",
            "anon_recipient" if HELL_CONFIG.anon_names else "recipient.name",
            "purpose.name",
            "category_name",
            "signed_colored_column",
            "signed_netto_colored_column",
            "tax_formatted_column",
        )
