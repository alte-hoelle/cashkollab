import calendar
from datetime import date

import pendulum
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, YEARLY, rrule
from pendulum import DateTime

from cashviz.helpers.types import MonthsList, MonthTuple


def date_to_pendulum(date_obj: date) -> DateTime:
    return pendulum.datetime(date_obj.year, date_obj.month, date_obj.day)


def month_count_since(since: date, with_current_month: bool = True) -> int:
    """list of years since the given date"""
    months = (pendulum.today() - date_to_pendulum(since)).in_months()
    if with_current_month:
        return int(months + 1)
    return int(months)


def years_since(since: date, with_current_year: bool = True) -> list[int]:
    """list of years since the given date"""
    years = [dx.year for dx in list(rrule(YEARLY, dtstart=since, until=date.today()))]
    return years


def month_list_since(since: date) -> MonthsList:
    """ " """
    return month_list_from_to(since, date.today())


def month_list_from_to(from_date: date, to_date: date) -> MonthsList:
    dates = list(rrule(MONTHLY, dtstart=from_date, until=to_date))
    return [
        MonthTuple(dt.year, dt.month, list(calendar.month_name)[dt.month])
        for dt in dates
    ]


def month_list_of_year(year: int) -> MonthsList:
    dates = list(rrule(MONTHLY, dtstart=date(year, 1, 1), until=date(year, 12, 31)))
    print(dates)
    return [
        MonthTuple(dt.year, dt.month, list(calendar.month_name)[dt.month])
        for dt in dates
    ]


def month_list_only_last_month() -> MonthsList:
    last_month = date.today() - relativedelta(months=1)
    return month_list_from_to(last_month, last_month)


def month_list_this_month() -> MonthsList:
    return month_list_from_to(date.today(), date.today())
