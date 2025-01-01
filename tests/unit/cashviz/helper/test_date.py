from datetime import date
from unittest.mock import MagicMock, patch

import pendulum
from dateutil.rrule import MONTHLY, rrule
from pendulum.tz.timezone import Timezone
from pytest import fixture
from pytest_mock import MockerFixture

from cashviz.helpers.date import (
    date_to_pendulum,
    month_count_since,
    month_list_from_to,
    month_list_of_year,
    month_list_only_last_month,
    month_list_since,
    month_list_this_month,
    years_since,
)
from cashviz.helpers.types import MonthTuple


@fixture
def datetime_date_mock(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("cashviz.helpers.date.date")
    mock.today.return_value = date(2022, 7, 23)
    mock.side_effect = lambda *args, **kw: date(*args, **kw)
    return mock


@fixture
def pendulum_date_mock(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("cashviz.helpers.date.pendulum.today")
    mock.return_value = pendulum.datetime(2022, 7, 23).date()
    return mock


def test_date_to_pendulum(datetime_date_mock: MagicMock, pendulum_date_mock) -> None:
    assert date_to_pendulum(date(2020, 12, 12)) == pendulum.DateTime(
        2020, 12, 12, 0, 0, 0, tzinfo=Timezone("UTC")
    )


def test_month_count_since(datetime_date_mock: MagicMock, pendulum_date_mock) -> None:
    assert month_count_since(date(2022, 1, 1), with_current_month=False) == 6
    assert month_count_since(date(2022, 1, 1)) == 7


def test_years_since(datetime_date_mock: MagicMock, pendulum_date_mock) -> None:
    assert years_since(date(2022, 1, 1)) == [2022]


def test_month_list_since(datetime_date_mock: MagicMock, pendulum_date_mock) -> None:
    since = date(2022, 5, 1)
    assert month_list_since(since) == [
        MonthTuple(2022, 5, "May"),
        MonthTuple(2022, 6, "June"),
        MonthTuple(2022, 7, "July"),
    ]


def test_month_list_from_to(datetime_date_mock: MagicMock, pendulum_date_mock) -> None:
    since = date(2021, 5, 1)
    until = date(2021, 7, 1)
    dates = [dt for dt in rrule(MONTHLY, dtstart=since, until=until)]
    months = [(dt.year, dt.month) for dt in dates]
    assert len(months) == len(dates)
    assert month_list_from_to(since, until) == [
        (2021, 5, "May"),
        (2021, 6, "June"),
        (2021, 7, "July"),
    ]


def test_month_list_of_year(datetime_date_mock: MagicMock, pendulum_date_mock) -> None:
    assert month_list_of_year(2022) == [
        MonthTuple(year=2022, month=1, name="January"),
        MonthTuple(year=2022, month=2, name="February"),
        MonthTuple(year=2022, month=3, name="March"),
        MonthTuple(year=2022, month=4, name="April"),
        MonthTuple(year=2022, month=5, name="May"),
        MonthTuple(year=2022, month=6, name="June"),
        MonthTuple(year=2022, month=7, name="July"),
        MonthTuple(year=2022, month=8, name="August"),
        MonthTuple(year=2022, month=9, name="September"),
        MonthTuple(year=2022, month=10, name="October"),
        MonthTuple(year=2022, month=11, name="November"),
        MonthTuple(year=2022, month=12, name="December"),
    ]


def test_month_list_only_last_month(
    datetime_date_mock: MagicMock, pendulum_date_mock
) -> None:
    assert month_list_only_last_month() == [MonthTuple(year=2022, month=6, name="June")]


def test_month_list_this_month(
    datetime_date_mock: MagicMock, pendulum_date_mock
) -> None:
    assert month_list_this_month() == [MonthTuple(year=2022, month=7, name="July")]
