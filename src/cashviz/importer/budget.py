from dataclasses import dataclass

from overrides import overrides

from cashviz.helpers.values import get_date
from cashviz.importer.base_importer import CsvImporter
from cashviz.models.budget import Budget
from cashviz.models.groups import Groups
from cashviz.models.purpose import Purpose


# pylint: disable=too-many-instance-attributes
@dataclass
class CSVBudgetDataclass:
    group_name: str
    purpose_name: str
    amount: str
    decided_date: str
    expire_date: str
    url: str

    def __post_init__(self) -> None:
        if self.group_name == "":
            self.group_name = "undefined"
        if self.purpose_name == "":
            self.purpose_name = "undefined"
        if self.amount == "":
            self.amount = "0.0"
        self.url = self.url.replace("\n", "")


class BudgetImporter(CsvImporter):
    @overrides
    def _import(self) -> None:
        # pylint: disable=no-member
        for line in self.lines:
            budgetdata = CSVBudgetDataclass(*line.split(";"))

            purpose, created = Purpose.objects.get_or_create(
                name=budgetdata.purpose_name
            )
            if created and self.verbose:
                print(f"Adding new Purpose({purpose.name})")

            group, created = Groups.objects.get_or_create(name=budgetdata.group_name)
            if created and self.verbose:
                print(f"Adding new Groups({group.name})")

            budget, created = Budget.objects.get_or_create(
                purpose__name=purpose.name,
                amount=budgetdata.amount,
                defaults={
                    "purpose": purpose,
                    "group": group,
                    "amount": budgetdata.amount,
                    "decided_date": get_date(budgetdata.decided_date),
                    "expire_date": get_date(budgetdata.expire_date),
                    "url": budgetdata.url,
                },
            )
            if created and self.verbose:
                print(
                    f"Adding new Budget ({budget.purpose.name=} {budget.group.name=})"
                )
