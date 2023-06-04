import pytest

import StocksMA.StocksMA as stm


def test_get_market_status() -> None:
    stat = stm.get_market_status()
    assert isinstance(stat, str)
