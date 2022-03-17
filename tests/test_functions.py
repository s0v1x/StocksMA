import src.StocksMA as stocks
import pandas as pd

def test_get_isin(example_company):
    assert stocks.get_isin(example_company) == ('Maroc Telecom', 'MA0000011488')

def test_get_market_status():
    stat = stocks.get_market_status()
    assert isinstance(stat, str)

def test_types(example_company):
    type1 = stocks.get_data_stock(example_company, '2021-02-13', '2022-02-07')
    assert isinstance(type1, pd.DataFrame)

    type2 = stocks.get_data(example_company, '2021-02-13')
    assert isinstance(type2, pd.DataFrame)

    type3 = stocks.get_quick_info(example_company)
    assert isinstance(type3, pd.DataFrame)

    type4 = stocks.get_data_intraday(example_company)
    assert isinstance(type4, pd.DataFrame)

    type5 = stocks.get_ask_bid(example_company)
    assert isinstance(type5, pd.DataFrame)

    type6 = stocks.get_balance_sheet(example_company)
    assert isinstance(type6, pd.DataFrame)

    type7 = stocks.get_income_statement(example_company)
    assert isinstance(type7, pd.DataFrame)

    type8 = stocks.get_cash_flow(example_company)
    assert isinstance(type8, pd.DataFrame)

    type9 = stocks.get_quote_table(example_company)
    assert isinstance(type9, pd.DataFrame)

    type10 = stocks.get_company_officers(example_company)
    assert isinstance(type10, pd.DataFrame)

    type11 = stocks.get_company_info(example_company)
    assert isinstance(type11, pd.DataFrame)