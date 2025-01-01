from typing import Any, Dict, List, Optional

from django.core.exceptions import ObjectDoesNotExist

from cashviz.helpers.date import month_list_since
from cashviz.helpers.tax import clean_from_tax
from cashviz.helpers.types import MonthsList
from cashviz.models.budget import Budget
from cashviz.models.journal_entry import JournalEntry
from cashviz.models.purpose import Purpose
from cashviz.settings import HELL_START_DATE
from config import HELL_CONFIG

ExpensesList = List[float]


# todo: refactor!
def get_credit_list(credit_type: Optional[str] = None) -> List[float]:
    try:
        credit_list = list(
            # pylint: disable=no-member
            JournalEntry.objects.filter(
                purpose=Purpose.objects.get(name=credit_type)
            ).values_list("signed", flat=True)
        )
        return [dx for dx in credit_list if dx > 0.0]
    except ObjectDoesNotExist:
        print(
            "Catched exception at Budget:Overview: Credit type does not exist: ",
            credit_type,
        )
        return []


def get_credit_pay_off_list(credit_type: Optional[str] = None) -> List[float]:
    try:
        pay_off_list = list(
            # pylint: disable=no-member
            JournalEntry.objects.filter(
                purpose=Purpose.objects.get(name=credit_type)
            ).values_list("signed", flat=True)
        )
        return [dx for dx in pay_off_list if dx < 0.0]
    except ObjectDoesNotExist:
        print(
            "Catched exception at Budget:Overview: Credit type does not exist: ",
            credit_type,
        )
        return [0.0]


# todo: refactor!
def get_expense_per_month(purpose: str, months: MonthsList) -> ExpensesList:
    expenses: ExpensesList = []
    for month in months:
        temp = 0.0
        # pylint: disable=no-member
        payments = JournalEntry.objects.filter(
            purpose=purpose, date__month=month.month, date__year=month.year
        )
        for payment in payments:
            temp += clean_from_tax(payment)
        expenses.append(temp)
    return expenses


# todo: refactor!
def get_chart_data() -> Dict[str, List[Any]]:
    purposes = list(Purpose.objects.all())  # pylint: disable=no-member
    budgetdata = []
    spentdata = []
    budgetnames = []
    groupnames = []
    labels = ["Budgetiert", "Ausgegeben"]

    for purpose in purposes:
        try:
            # pylint: disable=no-member
            budget = Budget.objects.get(purpose=purpose)
            budgetdata.append(budget.amount)
            budgetnames.append(budget.purpose.name)
            groupnames.append(budget.group.name)
            per_month_expanse = get_expense_per_month(
                purpose=purpose, months=month_list_since(HELL_START_DATE)
            )
            spentdata.append(-sum(per_month_expanse))
        except Exception:  # pylint: disable=broad-except
            pass  # print(f"ASD {error=}")

    credit_amounts = [sum(get_credit_list(dx)) for dx in HELL_CONFIG.credit.mapping]
    credit_pay_off_list = [
        get_credit_pay_off_list(HELL_CONFIG.credit.mapping[dx])
        for dx in HELL_CONFIG.credit.mapping
    ]
    credit_pay_off = [-sum(dx) for dx in credit_pay_off_list]

    return {
        "labels": labels,
        "spentdata": spentdata,
        "budgetdata": budgetdata,
        "budgetnames": budgetnames,
        "groupnames": groupnames,
        "credit_labels": list(HELL_CONFIG.credit.mapping.keys()),
        "credit_amounts": credit_amounts,
        "credit_pay_off": credit_pay_off,
        "credit_remaining": [
            (dx - dy) for (dx, dy) in zip(credit_amounts, credit_pay_off)
        ],
    }


# todo: refactor!
def get_overview_data() -> Dict[str, List[Any]]:
    chart_data = get_chart_data()
    budget = []
    credit = []
    for number in range(len(chart_data["budgetnames"])):
        budget.append(
            [
                chart_data["budgetnames"][number],
                chart_data["groupnames"][number],
                chart_data["budgetdata"][number],
                chart_data["spentdata"][number],
                chart_data["budgetdata"][number] - chart_data["spentdata"][number],
            ]
        )
    for number in range(len(chart_data["credit_labels"])):
        credit.append(
            [
                chart_data["credit_labels"][number],
                chart_data["credit_amounts"][number],
                chart_data["credit_pay_off"][number],
                chart_data["credit_remaining"][number],
            ]
        )
    return {"budget": budget, "credit": credit}
