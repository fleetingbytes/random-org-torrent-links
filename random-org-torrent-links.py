#!/usr/bin/env python

# Outputs torrent links for random.org pregenerated file archive


from datetime import datetime, MINYEAR
from argparse import ArgumentParser, ArgumentTypeError
from dataclasses import dataclass, field, InitVar
from typing import Generator

RANDOMORG_START_YEAR = 2006
RANDOMORG_START_MONTH = 3
MONTHS = range(1, 13)
LINK_TEMPLATE = "https://archive.random.org/download?file={}-bin.torrent"


@dataclass
class Date:
    year: int = field(init=False)
    month: int = field(init=False)
    date: InitVar[str]

    def __post_init__(self, date: str):
        try:
            year, month = map(int, date.split("-"))
        except ValueError:
            raise ArgumentTypeError(f"Invalid date format: {date}. Use YYYY-MM format.")
        now = datetime.now()
        if year not in range(RANDOMORG_START_YEAR, now.year + 1):
            raise ArgumentTypeError(f"Year must be between {RANDOMORG_START_YEAR} and {now.year}")
        if month not in MONTHS:
            raise ArgumentTypeError(f"Month must be between {next(iter(MONTHS))} and {next(reversed(MONTHS))}")
        if year >= now.year and month >= now.month:
            raise ArgumentTypeError(f"This month's torrent is not yet available")
        self.year = year
        self.month = month


def get_end_year_and_month() -> tuple[int, int]:
    now = datetime.now()
    end_year = now.year
    end_month = now.month
    first_month_of_the_year = next(iter(MONTHS))
    if end_month == first_month_of_the_year:
        last_month_of_the_year = next(reversed(MONTHS))
        end_month = last_month_of_the_year
        end_year = end_year if end_year == MINYEAR else end_year - 1
    return end_year, end_month - 1


def dates_to_download(start_year, start_month) -> Generator[str, None, None]:
    if start_year < RANDOMORG_START_YEAR:
        start_year = RANDOMORG_START_YEAR
    end_year, end_month = get_end_year_and_month()
    for year in range(start_year, end_year + 1):
        for month in MONTHS:
            if year == RANDOMORG_START_YEAR and month < RANDOMORG_START_MONTH:
                continue
            if year == start_year and month < start_month:
                continue
            if year == end_year and month > end_month:
                break
            date = f"{year}-{month:02d}" 
            yield date


def show_torrent_links(dates: Generator[str, None, None]) -> None:
    for date in dates:
        print(LINK_TEMPLATE.format(date))


if __name__ == "__main__":
    parser = ArgumentParser(prog="random-org-torrent-links", description="Outputs torrent links for random.org pregenerated file archive")
    parser.add_argument("start_date", type=Date, nargs="?", default=f"{RANDOMORG_START_YEAR}-{RANDOMORG_START_MONTH:02d}", help="date with which you would like to start (default: %(default)s)")
    date = parser.parse_args().start_date
    dates = dates_to_download(date.year, date.month)
    show_torrent_links(dates)
