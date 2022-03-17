import pandas as pd

import src.StocksMA as Stocks


def test_get_isin(example_company: str) -> None:
    assert Stocks.get_isin(example_company) == ('Maroc Telecom', 'MA0000011488')


def test_get_market_status() -> None:
    stat = Stocks.get_market_status()
    assert isinstance(stat, str)


def test_types(example_company: str) -> None:
    type1 = Stocks.get_data_stock(example_company, '2021-02-13', '2022-02-07')
    assert isinstance(type1, pd.DataFrame)

    type2 = Stocks.get_data(example_company, '2021-02-13')
    assert isinstance(type2, pd.DataFrame)

    type3 = Stocks.get_quick_info(example_company)
    assert isinstance(type3, pd.DataFrame)

    type4 = Stocks.get_data_intraday(example_company)
    assert isinstance(type4, pd.DataFrame)

    type5 = Stocks.get_ask_bid(example_company)
    assert isinstance(type5, pd.DataFrame)

    type6 = Stocks.get_balance_sheet(example_company)
    assert isinstance(type6, pd.DataFrame)

    type7 = Stocks.get_income_statement(example_company)
    assert isinstance(type7, pd.DataFrame)

    type8 = Stocks.get_cash_flow(example_company)
    assert isinstance(type8, pd.DataFrame)

    type9 = Stocks.get_quote_table(example_company)
    assert isinstance(type9, pd.DataFrame)

    type10 = Stocks.get_company_officers(example_company)
    assert isinstance(type10, pd.DataFrame)

    type11 = Stocks.get_company_info(example_company)
    assert isinstance(type11, pd.DataFrame)
