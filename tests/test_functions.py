import pytest

import StocksMA.StocksMA as stm


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
    obj = stm.get_isin(company)
    assert len(obj[1]) != 0
    assert isinstance(obj, tuple)


@pytest.mark.parametrize(
    "not_company",
    [
        "",
        "123",
        "aaaaa",
        "bank",
        "maroc",
        "agricol",
        "centrale",
    ],
)
@pytest.mark.xfail(raises=Exception)
def test_get_isin_not_company(not_company) -> None:
    stm.get_isin(not_company)


def test_get_market_status() -> None:
    stat = stm.get_market_status()
    assert isinstance(stat, str)
