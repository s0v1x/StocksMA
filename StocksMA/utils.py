import random
from functools import wraps

import requests

from StocksMA.exceptions import (
    CompanyNotFoundException,
    SectorNotFoundException,
)
from StocksMA.constants import SECTORS, USER_AGENTS, COMPANIES


def rand_agent() -> str:
    """Select a random User-Agent from USER_AGENTS

    Returns:
        str: User-Agent string
    """
    return random.choice(USER_AGENTS)


def remove_duplicates(string: str) -> str:
    """Remove duplicated words in a string

    Args:
        string (str): Names of items from income statement, balance sheet and cash flow Dataframes

    Returns:
        str: String without the duplicates
    """
    words = string.split()
    # HACK: remove duplicates keeping the order
    return " ".join(sorted(set(words), key=words.index))


def get_request(url: str) -> requests.models.Response:
    """Make a request

    Args:
        url (str): Resource URL

    Returns:
        requests.models.Response: JSON or HTML Response
    """
    headers = {"User-Agent": rand_agent()}
    return requests.get(url, headers=headers)


def check_company_existence(func):
    """
    This decorator is used to check if the company is in the list of companies
    Should be used with functions that take a company as **first** argument

    Raises:
        CompanyNotFoundException: The exception is raised when the company is not found in the COMPAINES dict.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        company = args[0]
        if (
            not isinstance(company, str)
            or company.upper() not in COMPANIES.keys()
        ):
            raise CompanyNotFoundException(
                f"Ticker {company} is not found, use get_tickers() to get a list of available tickers"
            )
        return func(*args, **kwargs)

    return wrapper


def check_sector_existence(func):
    """
    This decorator is used to check if the sector is in the list of sectors
    Should be used with functions that take a sector as **first** argument

    Raises:
        SectorNotFoundException: The exception is raised when the sector is not found in the SECTORS dict.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        sector = args[0]
        try:
            sector = list(
                filter(lambda s: sector.upper() in s, SECTORS.keys())
            )[0]
            return func(sector, **kwargs)
        except IndexError:
            raise SectorNotFoundException(
                f"Sector {sector} cannot be found, use get_sectors() to get a list of available sectors"
            )

    return wrapper
