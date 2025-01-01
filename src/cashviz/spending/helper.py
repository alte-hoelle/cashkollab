from cashviz.helpers.date import month_list_of_year
from cashviz.helpers.tax import clean_from_tax
from cashviz.helpers.types import MonthTuple, PurposeAmountDict
from cashviz.models.category import Category
from cashviz.models.journal_entry import JournalEntry
from config import HELL_CONFIG

YearlySpendingList = list[float]


def get_payment_sum_for_category(name: str, month: MonthTuple) -> float:
    # signed is the amount of the payment
    return sum(
        dx.signed
        for dx in list(
            JournalEntry.objects.filter(  # pylint: disable=no-member
                category=name, date__month=month.month, date__year=month.year
            )
        )
    )


def get_monthly_spending(month: MonthTuple, ignore: list[str]) -> dict[str, float]:
    # return {
    #   "category1", 123.23,
    #   "category2", 123.23
    # }
    #
    # pylint: disable=no-member
    result = {
        dx.name: get_payment_sum_for_category(dx, month)
        for dx in list(Category.objects.all())
        if dx.name not in ignore
    }
    total = 0.0
    for key in result:
        total += result[key]
    result["total"] = total
    return result


def get_yearly_spending(year: int, ignore: list[str]) -> list[dict[str, float]]:
    return [get_monthly_spending(dx, ignore) for dx in month_list_of_year(year)]


def get_yearly_spending_result(spendings: list[dict[str, float]]) -> list[float]:
    category = list(spendings[0].keys())
    results = {dx: 0.0 for dx in category}
    for month in spendings:
        for key, value in month.items():
            results[key] = results[key] + value
    return [dx[1] for dx in results.items()]


def get_single_month_by_target(
    month: int, year: int, ignore: list[str]
) -> PurposeAmountDict:
    amount: PurposeAmountDict = {}
    # pylint: disable=no-member
    for incident in JournalEntry.objects.filter(date__month=month, date__year=year):
        if incident.purpose.name not in HELL_CONFIG.spending.exclude:
            purpose = incident.purpose.name
            category = incident.category.name

            if purpose in amount:
                amount[purpose][category] += clean_from_tax(incident)
            else:
                # das is ziemlich stumpf lol
                # hier wäre zu klären ob nicht category einfach besser is weil er eh ne referenz anlegt
                amount[purpose] = {dx.name: 0.0 for dx in Category.objects.all()}
                amount[purpose]["final"] = 0.0
                amount[purpose][category] = clean_from_tax(incident)

    # Add everything up in the last column
    for _, value in amount.items():
        for key, value_ in value.items():
            if key in value and key != "final" and key not in ignore:
                value["final"] += value_

    for _, purpose in amount.items():
        for category in purpose:
            purpose[category] = round(purpose[category], 2)

    return amount


def get_result_amount_monthly(data: PurposeAmountDict) -> dict[str, float]:
    results: dict[str, float] = {}
    for _, category in data.items():
        for category_name, value in category.items():
            results[category_name] = 0.0
    results["final"] = 0.0

    for _, category in data.items():
        for category_name, value in category.items():
            results[category_name] += value
    return results
