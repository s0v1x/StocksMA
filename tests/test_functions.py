import pytest
from requests.models import Response

import StocksMA.StocksMA as Stocks
import StocksMA.utils as utils


@pytest.mark.parametrize(
    "company",
    [
        "CIH",
        "maroc telecom",
        "involys",
        "total",
        "telecom",
        "label",
        "central",
        "sothema",
        "MNG",
        "salaf",
        "CIH",
        "Auto Nejma",
    ],
)
def test_get_isin_company(company) -> None:
    obj = Stocks.get_isin(company)
    assert len(obj[1]) != 0
    assert isinstance(obj, tuple)


@pytest.mark.parametrize(
    "not_company",
    [
        "aaaaa",
        "123",
        "centrale",
        "maroc",
        "agricol" "",
        "bank",
    ],
)
@pytest.mark.xfail(raises=Exception)
def test_get_isin_not_company(not_company) -> None:
    Stocks.get_isin(not_company)


def test_get_market_status() -> None:
    stat = Stocks.get_market_status()
    assert isinstance(stat, str)
