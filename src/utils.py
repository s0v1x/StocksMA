import random
from functools import wraps

import requests

from . import COMPANIES, USER_AGENTS


def rand_agent() -> str:
    return random.choice(USER_AGENTS)


def remove_duplicates(string: str) -> str:
    words = string.split()
    # HACK: remove duplicates keeping the order
    return " ".join(sorted(set(words), key=words.index))


def get_request(url: str) -> requests.models.Response:
    headers = {"User-Agent": rand_agent()}
    return requests.get(url, headers=headers)


def check_company_existence(func):
    """
    This decorator is used to check if the company is in the list of companies
    Should be used with functions that take a company as **first** argument

    Raises:
        Exception: The exception is raised when the company is not found in
                the COMPAINES dict.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        company = args[0]
        if not isinstance(company, str) or company.upper() not in COMPANIES.keys():
            raise Exception(f"Ticker {company} is not found, use get_companies() to get a list of available companies")
        return func(*args, **kwargs)

    return wrapper
