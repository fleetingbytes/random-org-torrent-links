#!/usr/bin/env python

# Outputs torrent links for random.org pregenerated file archive

from argparse import ArgumentParser, ArgumentTypeError
from calendar import Month as Months
from collections.abc import Generator
from datetime import date, datetime, timedelta
from sys import stderr, exit


FIRST_DAY_OF_MONTH = 1
ERROR_INCORRECT_START_DATE = 1
RANDOMORG_START = date(2006, 3, FIRST_DAY_OF_MONTH)
LINK_TEMPLATE = "https://archive.random.org/download?file={}-bin.torrent"


def to_date(year_and_month: str) -> date:
    try:
        year_month_day = f"{year_and_month}-{FIRST_DAY_OF_MONTH:02d}"
        result = date.strptime(year_month_day, "%Y-%m-%d")
        return result
    except ValueError as exc:
        raise ArgumentTypeError(
            f'Invalid date format: "{year_and_month}". Use YYYY-MM format.'
        ) from exc


def validate_date(given_date: date) -> None:
    now = datetime.now()
    if given_date.year >= now.year and given_date.month >= now.month:
        raise ValueError(f"Torrent for {now.strftime('%Y-%m')} is not yet available.")


def exit_if_incorrect(start_date: date) -> None:
    try:
        validate_date(start_date)
    except ValueError as exc:
        print(exc, file=stderr)
        exit(ERROR_INCORRECT_START_DATE)


def get_previous_month(now: date) -> date:
    delta = timedelta(days=now.day)
    previous_month = now - delta
    previous_month = previous_month.replace(day=FIRST_DAY_OF_MONTH)

    return previous_month


def get_end_date() -> date:
    now = datetime.now()
    now = date(now.year, now.month, now.day)
    end_date = get_previous_month(now)

    return end_date


def downloadable_dates(start_date: date, end_date: date) -> Generator[date]:
    start_year = (
        start_date.year
        if start_date.year >= RANDOMORG_START.year
        else RANDOMORG_START.year
    )
    end_year = end_date.year

    all_dates = (
        date(year, month, FIRST_DAY_OF_MONTH)
        for year in range(start_year, end_year + 1)
        for month in Months
    )

    dates_since_randomorg_start = filter(
        lambda date: date >= RANDOMORG_START, all_dates
    )

    dates_since_start_date = filter(
        lambda date: date >= start_date, dates_since_randomorg_start
    )

    dates_until_end = filter(lambda date: date <= end_date, dates_since_start_date)

    yield from dates_until_end


def dates_to_download(
    start_date: date, end_date: date | None = None
) -> Generator[date]:
    if end_date is None:
        end_date = get_end_date()

    yield from downloadable_dates(start_date, end_date)


def torrent_link(year_and_month: date) -> str:
    return LINK_TEMPLATE.format(year_and_month)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="random-org-torrent-links",
        description="Outputs torrent links for random.org pregenerated file archive",
    )
    parser.add_argument(
        "start_date",
        type=to_date,
        nargs="?",
        default=RANDOMORG_START.strftime("%Y-%m"),
        help="date with which you would like to start (default: %(default)s)",
    )

    start_date = parser.parse_args().start_date
    exit_if_incorrect(start_date)

    dates = dates_to_download(start_date, None)
    for date_to_download in dates:
        print(torrent_link(date_to_download))
