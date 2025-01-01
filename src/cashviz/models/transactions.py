from django.core.validators import MinValueValidator
from django.db.models import PROTECT, CharField, DecimalField, ForeignKey, Model
from django.utils.translation import gettext_lazy as _


class Transactions(Model):
    CREDIT = "credit"
    DEBIT = "debit"

    TX_TYPE = [(CREDIT, _("Credit")), (DEBIT, _("Debit"))]

    type = CharField(max_length=10, choices=TX_TYPE, verbose_name=_("Tx Type"))
    journal_entry = ForeignKey(
        "django_ledger.JournalEntryModel",
        editable=False,
        related_name="txs",
        verbose_name=_("Journal Entry"),
        help_text=_("Journal Entry to be associated with this transaction."),
        on_delete=PROTECT,
    )

    account = ForeignKey(
        "django_ledger.AccountModel",
        related_name="txs",
        verbose_name=_("Account"),
        help_text=_(
            "Account from Chart of Accounts to be associated with this transaction."
        ),
        on_delete=PROTECT,
    )
    amount = DecimalField(
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        verbose_name=_("Amount"),
        help_text=_("Account of the transaction."),
        validators=[MinValueValidator(0)],
    )
    description = CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Tx Description"),
        help_text=_("A description to be included with this individual transaction"),
    )
