from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from overrides import overrides

from cashviz.helpers.names import clean_name
from cashviz.helpers.values import get_date
from cashviz.importer import CsvImporter
from cashviz.models.account import Account
from cashviz.models.person import Person


@dataclass
class CSVPersonDataclass:
    name: str
    member_date: str
    stop_member_date: str
    supporter_date: str
    stop_support_date: str
    support_amount: str
    membership_fee_amount: str = "0.0"
    iban: str = ""
    bic: str = ""
    email: str = ""

    def __post_init__(self) -> None:
        self.bic = self.bic.replace("\n", "")


class PersonImporter(CsvImporter):
    @overrides
    def _import(self) -> None:
        # pylint: disable=no-member
        for line in self.lines:
            persondata = CSVPersonDataclass(*line.split(";"))
            supporter_date = persondata.supporter_date
            stop_support_date = persondata.stop_support_date
            member_date = persondata.member_date
            stop_member_date = persondata.stop_member_date

            support_ammount = persondata.support_amount
            support_amount = (
                0 if not self._check(support_ammount) else int(support_ammount)
            )

            is_supporter = self._check(supporter_date) and not self._check(
                stop_support_date
            )
            is_member = self._check(member_date) and not self._check(stop_member_date)
            if persondata.membership_fee_amount == "":
                persondata.membership_fee_amount = "0.0"

            (
                account,
                created,
            ) = Account.objects.get_or_create(  # pylint: disable=no-member
                IBAN=persondata.iban,
                BIC=persondata.bic,
                defaults={
                    "comment": persondata.name,
                },
            )
            if created and self.verbose:
                print(f"Adding new Account({account.comment=})")
            person, _ = Person.objects.get_or_create(
                clean_name=clean_name(persondata.name),
                defaults={
                    "name": persondata.name,
                    "is_supporter": is_supporter,
                    "supporter_since": self._date(supporter_date),
                    "not_supporter_since": self._date(stop_support_date),
                    "is_member": is_member,
                    "member_since": self._date(member_date),
                    "not_member_since": self._date(stop_member_date),
                    "support_amount": support_amount,
                    "membership_fee": float(persondata.membership_fee_amount),
                },
            )
            person.account.add(account)
            if self.verbose:
                print(f"Adding new Person({person.name=})")
            person.set_fee(member_date, float(persondata.membership_fee_amount))
            if self._check(stop_member_date):
                person.set_fee(stop_member_date, 0.0)
            person.set_support(supporter_date, support_amount)
            if self._check(stop_support_date):
                person.set_support(stop_support_date, 0.0)
            person.save()

    # pylint: disable=no-self-use
    def _check(self, date_str: str) -> bool:
        return date_str not in ["", None]

    def _date(self, date_str: str) -> Optional[datetime]:
        if self._check(date_str):
            # fuckoff mypy -.-
            value: Optional[datetime] = get_date(date_str)
            return value
        return None
