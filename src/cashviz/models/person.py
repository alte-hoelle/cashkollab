from typing import Any

import pendulum
from django.apps import apps
from django.db.models import (
    BooleanField,
    CharField,
    DateField,
    FloatField,
    Manager,
    ManyToManyField,
    Model,
    Q,
    QuerySet,
    TextField,
)
from django.utils.safestring import SafeString

from cashviz.helpers.date import date_to_pendulum, month_count_since
from cashviz.helpers.html import float_colored_html
from cashviz.helpers.values import get_date
from cashviz.models.account import Account
from cashviz.settings import FEE_START_DATE, NO_FEE_2019


class PersonQuerySet(QuerySet):
    pass


class MemberManager(Manager):
    def get_queryset(self) -> QuerySet:
        return PersonQuerySet(self.model, using=self._db).filter(Q(is_member=True))


class SupporterManager(Manager):
    def get_queryset(self) -> QuerySet:
        return PersonQuerySet(self.model, using=self._db).filter(Q(is_supporter=True))


class MemberAndSupporterManager(Manager):
    def get_queryset(self) -> QuerySet:
        return PersonQuerySet(self.model, using=self._db).filter(
            Q(is_supporter=True) | Q(is_member=True)
        )


class Person(Model):
    name = CharField(max_length=100, verbose_name="Person Name")
    account = ManyToManyField(Account)
    is_supporter = BooleanField(default=False)
    supporter_since = DateField(default=None, null=True, blank=True)
    not_supporter_since = DateField(default=None, null=True, blank=True)
    is_member = BooleanField(default=False)
    member_since = DateField(default=None, null=True, blank=True)
    not_member_since = DateField(default=None, null=True, blank=True)
    support_amount = FloatField(default=0.0)
    membership_fee = FloatField(default=0.0)
    clean_name = CharField(max_length=100)
    comment = TextField(default="")

    # managers
    objects = Manager()
    member_and_supporter = MemberAndSupporterManager()
    supporter = SupporterManager()
    member = MemberManager()

    def __str__(self) -> str:
        return f"{self.name}"

    def anon_name(self) -> str:
        return "anon"

    def __sum_signed(self, purpuse_name: str) -> float:
        payment_model = apps.get_model("cashviz.JournalEntry")
        payments = payment_model.member_and_supporter.filter(
            purpose__name=purpuse_name
        ).filter(Q(recipient=self) | Q(recipient_account__in=self.account.all()))
        return float(sum(dx.signed for dx in payments))

    def __due_table(self, type_str: str) -> list[float]:
        changes_model = apps.get_model("cashviz.BillingChanges")
        changes = changes_model.objects.filter(
            type=type_str, person__name=self.name
        ).values()
        if not changes:
            return []
        changes = sorted(changes, key=lambda d: d["date"])  # type: ignore[no-any-return]

        start_date = (
            FEE_START_DATE
            if changes[0]["date"].year == 2019 and NO_FEE_2019
            else changes[0]["date"]
        )

        total_months = month_count_since(start_date)
        amount_table = [0.0] * total_months

        for change in changes:
            changes_date = (
                FEE_START_DATE
                if change["date"].year == 2019 and NO_FEE_2019
                else change["date"]
            )
            months = month_count_since(changes_date)
            for index in range(months):
                amount_table[index] = change["amount"]
        return amount_table

    def payed_fees(self) -> float:
        return self.__sum_signed("Mitgliedsbeitrag")

    def payed_support(self) -> float:
        return self.__sum_signed("Unterstützung")

    def support_due(self) -> float:
        support_table = self.__due_table("support")
        return sum(support_table)

    def member_fees_due(self) -> float:
        fee_table = self.__due_table("fee")
        return sum(fee_table)

    def member_fees_open(self) -> float:
        return self.member_fees_due() - self.payed_fees()

    def member_fees_open_as_html(self) -> SafeString:
        return SafeString(float_colored_html(-self.member_fees_open()))

    def support_open(self) -> float:
        return self.support_due() - self.payed_support()

    def support_open_as_html(self) -> SafeString:
        return SafeString(float_colored_html(-self.support_open()))

    def support_and_fee_table(self) -> list[list[float | str]]:
        support = self.__due_table("support")
        fee = self.__due_table("fee")
        payments = self.fee_and_support_payments()
        table_length = len(support) if len(support) > len(fee) else len(fee)
        table = []
        for index in range(table_length):
            date_format = "Y_M"
            period = pendulum.today().subtract(months=index)  # type: ignore[no-untyped-call]
            date_str = period.format(date_format)
            payments_in_month = [
                dx["signed"]
                for dx in payments
                if date_to_pendulum(dx["date"]).format(date_format) == date_str
            ]
            support_amount = 0.0 if index >= len(support) else support[index]
            fee_amount = 0.0 if index >= len(fee) else fee[index]
            if date_str[:4] == "2019" and NO_FEE_2019:
                fee_amount = 0.0
            table.append([date_str, support_amount, fee_amount, sum(payments_in_month)])

        # now lets hack a bit... we must calc from the end, so we reverse the table
        table.reverse()
        promised = 0.0
        payed = 0.0
        for index in range(table_length):
            promised += table[index][1] + table[index][2]
            payed += table[index][3]
            table[index].append(payed - promised)

        # reverse it back
        table.reverse()
        return table

    def fee_and_support_changes(self) -> list[dict[str, Any]]:
        changes_model = apps.get_model("cashviz.BillingChanges")
        changes = changes_model.objects.filter(person=self)
        return sorted(changes.values(), key=lambda d: d["date"], reverse=True)  # type: ignore[no-any-return]

    def fee_and_support_payments(self) -> list[dict[str, Any]]:
        payment_model = apps.get_model("cashviz.JournalEntry")
        payments = payment_model.member_and_supporter.filter(
            Q(recipient=self) | Q(recipient_account__in=self.account.all())
        ).filter(Q(purpose__name="Mitgliedsbeitrag") | Q(purpose__name="Unterstützung"))
        return sorted(payments.values(), key=lambda d: d["date"], reverse=True)  # type: ignore[no-any-return]

    def set_fee(self, date_str: str, amount: float) -> None:
        self._add_billing_change(date_str, type_str="fee", amount=amount)

    def set_support(self, date_str: str, amount: float) -> None:
        self._add_billing_change(date_str, type_str="support", amount=amount)

    def _add_billing_change(self, date_str: str, type_str: str, amount: float) -> None:
        if date_str not in ["", None]:
            changes_model = apps.get_model("cashviz.BillingChanges")
            changes = changes_model(
                type=type_str, date=get_date(date_str), amount=amount, person=self
            )
            changes.save()
