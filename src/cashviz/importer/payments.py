from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.db.models import Q
from overrides import overrides

from cashviz.helpers.names import clean_name
from cashviz.helpers.values import get_date, get_float, get_int
from cashviz.importer import CsvImporter
from cashviz.models.account import Account
from cashviz.models.category import Category
from cashviz.models.journal_entry import JournalEntry
from cashviz.models.person import Person
from cashviz.models.purpose import Purpose


# pylint: disable=too-many-instance-attributes
@dataclass
class CSVJournalEntryDataclass:
    journal_number: int
    own_account: str
    own_iban: str
    own_bic: str
    own_bank: str
    booking_date: str
    valuta_date: str
    recipient: str
    iban: str
    bic: str
    textkey: str
    booking_text: str
    signed_value: str
    currency: str
    saldo: str
    purpose: str = ""
    category: str = ""
    comment: str = ""
    taxes: str = ""
    creditor_id: str = ""
    mandate_reference: str = ""

    def __post_init__(self) -> None:
        if self.category == "":
            self.category = "undefined"
        if self.purpose == "":
            self.purpose = "undefined"
        if self.recipient == "":
            self.recipient = "undefined"
        self.mandate_reference = self.mandate_reference.replace("\n", "")


class JournalEntryImporter(CsvImporter):
    @overrides
    def _import(self) -> None:
        linecount = 0
        for line in self.lines:
            if "Buchungstag" in line:
                if self.verbose:
                    print(f"[payment importer] found csv header {line=})")
                continue
            line_split = line.split(";")
            if line_split[0] != "":
                paymentdata = CSVJournalEntryDataclass(*line.split(";"))

                valuta_date = get_date(paymentdata.valuta_date)
                booking_date = get_date(paymentdata.booking_date)
                if valuta_date is None and booking_date is None:
                    # todo: error weil beide Dates None!
                    pass
                valuta_date = valuta_date if valuta_date is not None else booking_date
                booking_date = booking_date if booking_date is not None else valuta_date

                (
                    purpose,
                    created,
                ) = Purpose.objects.get_or_create(  # pylint: disable=no-member
                    name=paymentdata.purpose
                )
                if created and self.verbose:
                    print(f"[payment importer] Adding new Purpose({purpose.name=})")

                # is our own account in the account table?
                own_account, created = Account.objects.get_or_create(
                    IBAN=paymentdata.own_iban,
                    BIC=paymentdata.own_bic,
                    defaults={
                        "bank_name": paymentdata.own_bank,
                        "comment": "hoellen konto",
                    },
                )
                if created and self.verbose:
                    print(
                        f"[payment importer] Adding new Account({own_account.comment=})"
                    )

                # is the recipient account in the account table?
                (
                    recip_account,
                    created,
                ) = Account.objects.get_or_create(  # pylint: disable=no-member
                    IBAN=paymentdata.iban,
                    BIC=paymentdata.bic,
                    defaults={
                        "comment": paymentdata.recipient,
                    },
                )
                if created and self.verbose:
                    print(
                        f"[payment importer] Adding new Account({recip_account.comment=})"
                    )

                try:
                    # pylint: disable=no-member
                    person, created = Person.objects.filter(
                        Q(name__iexact=paymentdata.recipient)
                        | Q(account__IBAN=paymentdata.iban)
                    ).get_or_create(
                        clean_name=clean_name(paymentdata.recipient),
                        defaults={
                            "name": paymentdata.recipient,
                            "is_supporter": False,
                            "supporter_since": None,
                            "not_supporter_since": None,
                            "is_member": False,
                            "member_since": None,
                            "not_member_since": None,
                            "support_amount": 0,
                        },
                    )
                    if created:
                        if self.verbose:
                            print(f"[payment importer] person created: {person.name}")
                        person.account.add(recip_account)
                        person.save()

                    payment, created = JournalEntry.objects.get_or_create(
                        date=booking_date,
                        valuta=valuta_date,
                        textkey=paymentdata.textkey,
                        recipient=person,
                        comment=paymentdata.booking_text,
                        currency=paymentdata.currency,
                        signed=get_float(paymentdata.signed_value),
                        purpose=purpose,
                        category=Category.objects.get(  # pylint: disable=no-member
                            identifier=paymentdata.category
                        ),
                        taxes=get_int(paymentdata.taxes),
                        recipient_account=recip_account,
                        account=own_account,
                    )
                    if created and self.verbose:
                        print(
                            f"[payment importer] Adding new JournalEntry: {payment.comment=}"
                        )
                    elif self.verbose:
                        print(f"[payment importer] payment was in databank {payment=}")
                    linecount += 1
                except Exception as expection:  # pylint: disable=broad-except
                    print(f"[payment importer] {expection=}")
                    print(f"[payment importer] {line=}")
                    print(f"[payment importer] {paymentdata.category=}")
                    print(f"[payment importer] {valuta_date=}")
                    print(f"[payment importer] {booking_date=}")
                    continue
        print(f"[payment importer] imported {linecount} lines")

    # pylint: disable=no-self-use
    def _check(self, date_str: str) -> bool:
        return date_str not in ["", None]

    def _date(self, date_str: str) -> Optional[datetime]:
        if self._check(date_str):
            # fuckoff mypy -.-
            value: Optional[datetime] = get_date(date_str)
            return value
        return None
