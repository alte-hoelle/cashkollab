from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    IntegerField,
    Manager,
    Model,
    Q,
    QuerySet,
)
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.safestring import SafeString

from cashviz.helpers.html import float_colored_html, tax_formatter
from cashviz.models.account import Account
from cashviz.models.category import Category
from cashviz.models.person import Person
from cashviz.models.purpose import Purpose


class MemberAndSupporterManager(Manager):
    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .filter(Q(recipient__is_member=True) | Q(recipient__is_supporter=True))
        )


class JournalEntry(Model):
    account = ForeignKey(
        Account, on_delete=CASCADE, default=None, related_name="account"
    )
    date = DateField()
    valuta = DateField()
    textkey = CharField(max_length=30)
    recipient = ForeignKey(Person, on_delete=CASCADE, default=None)
    recipient_account = ForeignKey(
        Account, on_delete=CASCADE, default=None, related_name="recipient_account"
    )
    comment = CharField(max_length=100)
    currency = CharField(max_length=30)
    signed = FloatField(max_length=30, verbose_name="amount")  # value
    purpose = ForeignKey(Purpose, on_delete=CASCADE, default=None)
    category = ForeignKey(Category, on_delete=CASCADE, default=None)
    taxes = IntegerField(
        default=0,
    )

    objects = Manager()
    member_and_supporter = MemberAndSupporterManager()

    def __str__(self) -> str:
        return str(self.recipient.name)

    def signed_netto(self) -> float:
        return (
            self.signed
            if self.taxes == 0
            else round(self.signed / (self.taxes / 100 + 1), 2)
        )

    def signed_colored(self) -> SafeString:
        return SafeString(float_colored_html(self.signed))

    def signed_netto_colored(self) -> SafeString:
        return SafeString(float_colored_html(self.signed_netto()))

    def taxes_formatted(self) -> SafeString:
        return SafeString(tax_formatter(self.taxes))

    # noinspection PyMethodMayBeStatic
    def anon_recipient(self) -> str:
        return "anon"

    def set_purpose(self) -> str:
        def active(name: str) -> str:
            return "selected" if self.purpose.name == name else ""

        options = [
            f"<option {active(dx.name)} value='{reverse_lazy('admin:admin_payment_set_purpose', args=[self.pk, dx.name])}'><a href='#'>{dx.name}</a></option>"
            for dx in list(Purpose.objects.all())  # pylint: disable=no-member
        ]
        return format_html(
            f'<select onchange="location = this.value;" name="forma">{options}</select>'
        )

    set_purpose.short_description = "purpose"  # type: ignore[attr-defined]

    def short_recipient(self) -> str:
        return str(self.recipient.name[:30])

    set_purpose.short_description = "recipient"  # type: ignore[attr-defined]

    def short_comment(self) -> str:
        return str(self.comment)[:100]

    set_purpose.short_description = "comment"  # type: ignore[attr-defined]
