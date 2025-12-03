#!/usr/bin/env python

# Outputs torrent links for random.org pregenerated file archive


from argparse import ArgumentParser, ArgumentTypeError
from collections.abc import Generator
from datetime import datetime, MINYEAR, date as dt_date

RANDOMORG_START_YEAR = 2006
RANDOMORG_START_MONTH = 3
MONTHS = range(1, 13)
LINK_TEMPLATE = "https://archive.random.org/download?file={}-bin.torrent"


def to_date(s: str) -> dt_date:
    try:
        year, month = map(int, s.split("-"))
    except ValueError:
        raise ArgumentTypeError(
            f"Invalid date format: {date}. Use YYYY-MM format."
        ) from ValueError
    if month not in MONTHS:
        raise ArgumentTypeError(
            f"Month must be between {next(iter(MONTHS))} and {next(reversed(MONTHS))}"
        )
    result = dt_date(year, month, 1)
    return result


def correct_end_month_and_year_if_in_january(month: int, year: int) -> tuple[int, int]:
    january = next(iter(MONTHS))
    if month == january:
        december = next(reversed(MONTHS))
        month = december
        year = year if year == MINYEAR else year - 1
    return month, year


def get_end_date() -> dt_date:
    now = datetime.now()
    end_year = now.year
    end_month = now.month

    result = end_year, end_month - 1
    result = correct_end_month_and_year_if_in_january(*result)

    end_date = dt_date(*result, 1)

    return end_date


def downloadable_dates(start_date: date, end_date: date) -> Generator[dt_date]:
    randomorg_start = dt_date(RANDOMORG_START_YEAR, RANDOMORG_START_MONTH, 1)

    start_year = start_date.year
    end_year = end_date.year

    all_dates = (
        dt_date(year, month, 1)
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
    start_date: date, end_date: dt_date | None = None
) -> Generator[dt_date]:
    if end_date is None:
        end_date = get_end_date()

    yield from downloadable_dates(start_date, end_date)


def torrent_link(date: dt_date) -> str:
    return LINK_TEMPLATE.format(date)


def validate_date(date: dt_date) -> None:
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
        type=to_date,
        nargs="?",
        default=f"{RANDOMORG_START_YEAR}-{RANDOMORG_START_MONTH:02d}",
        help="date with which you would like to start (default: %(default)s)",
    )

    start_date = parser.parse_args().start_date
    validate_date(start_date)

    dates = dates_to_download(start_date)
    for date in dates:
        print(torrent_link(date))
