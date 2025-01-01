from cashviz.budget.helper import ExpensesList
from cashviz.helpers.tax import clean_from_tax
from cashviz.helpers.types import MonthsList
from cashviz.models.journal_entry import JournalEntry


def get_expense_per_month(purpose: str, months: MonthsList) -> ExpensesList:
    expenses: ExpensesList = []
    for month in months:
        temp = 0.0
        # pylint: disable=no-member
        payments = JournalEntry.objects.filter(
            purpose=purpose, date__month=month[1], date__year=month[0]
        )
        for payment in payments:
            temp += clean_from_tax(payment)
        expenses.append(temp)
    return expenses
