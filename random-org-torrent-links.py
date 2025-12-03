#!/usr/bin/env python

# Outputs torrent links for random.org pregenerated file archive


from argparse import ArgumentParser, ArgumentTypeError
from collections.abc import Generator
from dataclasses import dataclass, field, InitVar
from datetime import datetime, MINYEAR, date as dt_date
from typing import Self

RANDOMORG_START_YEAR = 2006
RANDOMORG_START_MONTH = 3
MONTHS = range(1, 13)
LINK_TEMPLATE = "https://archive.random.org/download?file={}-bin.torrent"


@dataclass
class Date:
    year: int = field(init=False)
    month: int = field(init=False)
    _date: dt_date = field(init=False, repr=False)
    date: InitVar[str]

    def __post_init__(self, date: str):
        try:
            year, month = map(int, date.split("-"))
        except ValueError:
            raise ArgumentTypeError(
                f"Invalid date format: {date}. Use YYYY-MM format."
            ) from ValueError
        if month not in MONTHS:
            raise ArgumentTypeError(
                f"Month must be between {next(iter(MONTHS))} and {next(reversed(MONTHS))}"
            )
        self.year = year
        self.month = month
        self._date = dt_date(year, month, 1)

    @classmethod
    def from_values(cls, year: int, month: int) -> Self:
        result = cls(f"{year}-{month:02d}")
        return result

    def __hash__(self) -> int:
        return self._date.__hash__()

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02d}"

    def __lt__(self, other: Self) -> bool:
        return self._date < other._date

    def __le__(self, other: Self) -> bool:
        return self._date <= other._date

    def __gt__(self, other: Self) -> bool:
        return self._date > other._date

    def __ge__(self, other: Self) -> bool:
        return self._date >= other._date

    def __eq__(self, other: Self) -> bool:
        return self._date == other._date


def correct_end_month_and_year_if_in_january(month: int, year: int) -> tuple[int, int]:
    january = next(iter(MONTHS))
    if month == january:
        december = next(reversed(MONTHS))
        month = december
        year = year if year == MINYEAR else year - 1
    return month, year


def get_end_date() -> Date:
    now = datetime.now()
    end_year = now.year
    end_month = now.month

    result = end_year, end_month - 1
    result = correct_end_month_and_year_if_in_january(*result)

    end_date = Date.from_values(*result)

    return end_date


def downloadable_dates(start_date: Date, end_date: Date) -> Generator[Date]:
    randomorg_start = Date.from_values(RANDOMORG_START_YEAR, RANDOMORG_START_MONTH)

    start_year = start_date.year
    end_year = end_date.year

    all_dates = (
        Date.from_values(year, month)
        for year in range(start_year, end_year + 1)
        for month in MONTHS
    )

    dates_since_randomorg_start = filter(
        lambda date: date >= randomorg_start, all_dates
    )

    dates_since_start_date = filter(
        lambda date: date >= start_date, dates_since_randomorg_start
    )

    dates_until_end = filter(lambda date: date <= end_date, dates_since_start_date)

    yield from dates_until_end


def dates_to_download(
    start_date: Date, end_date: Date | None = None
) -> Generator[Date]:
    if end_date is None:
        end_date = get_end_date()

    yield from downloadable_dates(start_date, end_date)


def torrent_link(date: Date) -> str:
    return LINK_TEMPLATE.format(date)


def validate_date(date: Date) -> None:
    now = datetime.now()
    if start_date.year >= now.year and start_date.month >= now.month:
        raise ValueError("This month's torrent is not yet available")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="random-org-torrent-links",
        description="Outputs torrent links for random.org pregenerated file archive",
    )
    parser.add_argument(
        "start_date",
        type=Date,
        nargs="?",
        default=f"{RANDOMORG_START_YEAR}-{RANDOMORG_START_MONTH:02d}",
        help="date with which you would like to start (default: %(default)s)",
    )

    start_date = parser.parse_args().start_date
    validate_date(start_date)

    dates = dates_to_download(start_date)
    for date in dates:
        print(torrent_link(date))
