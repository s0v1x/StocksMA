import random

import requests

from . import COMPANIES, USER_AGENTS


def rand_agent() -> str:
    return random.choice(USER_AGENTS)


def remove_duplicates(string: str) -> str:
    words = string.split()
    # HACK: remove duplicates keeping the order
    return " ".join(sorted(set(words), key=words.index))

# TODO: Might be converted into a decorator
def check_company(company: str) -> None:
    if not isinstance(company, str) or company.upper() not in COMPANIES.keys():
        raise Exception(
            "Ticker {company} is not found, use get_companies()".format(company=company)
        )


def get_request(url: str) -> requests.models.Response:
    headers = {"User-Agent": rand_agent()}
    return requests.get(url, headers=headers)
