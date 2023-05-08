import json
import re
import warnings
from datetime import datetime
from typing import Dict, List, Tuple, Union, Optional

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

import StocksMA.utils as utils
from StocksMA.constants import SECTORS, COMPANIES
from StocksMA.exceptions import CompanyNotFoundException


# Enabling warnings
warnings.simplefilter("always")

T_ed = Union[str, None]


def get_tickers(as_df: bool = False) -> Optional[pd.DataFrame]:
    """Show available tickers with the full name of the company.

    Args:
        as_df :bool: When the input argument is True, the function will generate a DataFrame that includes
               the list of available tickers along with the complete company name for each ticker.

    Raises:
        ValueError: The argument as_df must be a boolean value.

    Returns:
        Optional[pd.DataFrame]: A DataFrame that that includes the list of available tickers along with
                                the complete company name for each ticker.
    """
    if not isinstance(as_df, bool):
        raise ValueError(
            f"The argument as_df must be a boolean value of either True or False, but we received a value of type {type(as_df).__name__} instead."
        )

    if as_df:
        return pd.DataFrame(
            {
                "Ticker": COMPANIES.keys(),
                "Name": [info.name for info in COMPANIES.values()],
            }
        ).set_index("Ticker")

    for ticker, info in COMPANIES.items():
        print(ticker, "/", info.name)
    return


def get_isin(company: str) -> Tuple[str, str]:
    """Get International Securities Identification Number (ISIN)
    of a given Moroccan company

    Args:
        company (str): Company name or ticker symbol (e.g. 'maroc telecom', 'MNG')

    Raises:
        ValueError: Company argument is not a string.
        CompanyNotFoundException: Company cannot be found.

    Returns:
        Tuple: (Company full name, Company ISIN)
    """
    if not type(company) is str:
        raise ValueError("Company argument must be of string data type")

    for ticker, company_info in COMPANIES.items():
        if (company.upper() == ticker.upper()) or (
            company.upper() == company_info.name.upper()
        ):
            return company_info.name, company_info.isin

    raise CompanyNotFoundException(
        f"Company {company} cannot be found, use get_tickers() to get a list of available tickers"
    )


def get_data_stock(
    company: str, start_date: str, end_date: T_ed
) -> pd.DataFrame:
    """Get historical OHLCV data for a given symbol
    Args:
        company (str): Company name or ticker symbol(e.g. 'maroc telecom', 'MNG')
        start_date (str): (YYYY-MM-DD) Starting date to pull data from, limited to a maximum of six year
        end_date (T_ed): (YYYY-MM-DD) Ending date

    Returns:
        pd.DataFrame: Dataframe of historical OHLCV data
    """
    name, isin = get_isin(company)
    url = (
        "https://medias24.com/content/api?method=getStockOHLC&ISIN="
        + isin
        + "&format=json"
    )

    request_data = utils.get_request(url)
    data = json.loads(request_data.content)
    data = pd.DataFrame(
        data["result"],
        columns=["Date", "Open", "High", "Low", "Close", "Volume"],
    )
    data.index = pd.to_datetime(
        data.Date.apply(lambda x: datetime.fromtimestamp(x / 1000.0).date())
    )
    data = data.loc[lambda x: (start_date <= x.index) & (x.index <= end_date)]
    data.set_index(
        pd.MultiIndex.from_product(
            [[name], data.index], names=["Company", "Date"]
        ),
        inplace=True,
    )
    data.drop(["Date"], axis=1, inplace=True)

    return data


def get_price_data(
    tickers: Union[str, List[str]],
    start_date: str,
    end_date: T_ed = datetime.now().strftime("%Y-%m-%d"),
) -> pd.DataFrame:
    """Get historical OHLCV data for a given symbol(s)

    Args:
        tickers (Union[str, List[str]]): List or str of companies names or ticker symbols(e.g. ['maroc telecom', 'MNG'] or 'CIH')
        start_date (str): (YYYY-MM-DD) Starting date to pull data from, limited to a maximum of six year
        end_date (T_ed, optional): (YYYY-MM-DD) Ending date. Defaults to the current local date

    Raises:
        ValueError: end_date is greater than today's date
        ValueError: start_date is limited to a maximum of six year

    Returns:
        pd.DataFrame: Dataframe of historical OHLCV data
    """
    today: datetime = datetime.now()
    six_year_from_now: datetime = today - relativedelta(years=6)

    if datetime.strptime(end_date, "%Y-%m-%d") > today:
        raise ValueError(
            "end_date is greater than {today}".format(
                today=today.strftime("%Y-%m-%d")
            )
        )
    if datetime.strptime(start_date, "%Y-%m-%d") < six_year_from_now:
        raise ValueError("start_date is limited to a maximum of six year")

    if isinstance(tickers, list):
        dataframes: List = [
            get_data_stock(t, start_date, end_date) for t in tickers
        ]
        return pd.concat(dataframes, sort=True)
    else:
        return get_data_stock(tickers, start_date, end_date)


def get_session_info(company: str) -> pd.DataFrame:
    """Get data related to the current trading session of a given symbol

    Args:
        company (str): Company name or ticker symbol(e.g. 'maroc telecom', 'MNG')

    Returns:
        pd.DataFrame: Dataframe of session data
    """
    pattern = re.compile(r"^(MA00000)\d+$")
    if not pattern.match(company):
        _, isin = get_isin(company)
    else:
        isin = company
    url = (
        "https://medias24.com/content/api?method=getStockInfo&ISIN="
        + isin
        + "&format=json"
    )

    request_data = utils.get_request(url)
    data = json.loads(request_data.content)["result"]
    data = pd.DataFrame(data.items()).T
    cols = [
        "Name",
        "Name_2",
        "ISIN",
        "Number of Shares",
        "Close",
        "Previous Close",
        "Market Cap",
        "Quotation Datetime",
        "Change",
        "Volume Change",
        "Volume in Shares",
        "Volume",
        "Open",
        "Low",
        "High",
    ]
    data.columns = cols
    data.drop(data.index[0], inplace=True)

    return data


def get_data_intraday(company: str) -> pd.DataFrame:
    """Get intraday price data of a given symbol

    Args:
        company (str): Company name or ticker symbol(e.g. 'maroc telecom', 'MNG')

    Returns:
        pd.DataFrame: Dataframe of intraday price data
    """
    _, isin = get_isin(company)
    date = (
        get_session_info(isin)["Quotation Datetime"]
        .to_string(index=False)
        .replace("à", "")
    )
    url = (
        "https://medias24.com/content/api?method=getStockIntraday&ISIN="
        + isin
        + "&format=json"
    )

    request_data = utils.get_request(url)
    data = json.loads(request_data.content)["result"][0]
    data = pd.DataFrame(data)
    data.index = pd.to_datetime(
        data.labels.apply(
            lambda x: datetime.combine(
                datetime.strptime(date, "%d/%m/%Y  %H:%M").date(),
                datetime.strptime(x, "%H:%M").time(),
            )
        )
    ).rename("Datetime")
    data.drop("labels", axis=1, inplace=True)
    data.columns = ["Price"]

    return data


def get_ask_bid(company: str) -> pd.DataFrame:
    """Get ask bid data of a given symbol

    Args:
        company (str): Company name or ticker symbol(e.g. 'maroc telecom', 'MNG')

    Returns:
        pd.DataFrame: Dataframe of ask bid data
    """
    _, isin = get_isin(company)
    url = f"https://medias24.com/content/api?method=getBidAsk&ISIN={isin}&format=json"

    request_data = utils.get_request(url)
    data = json.loads(request_data.content)["result"]["orderBook"]
    data = pd.DataFrame(data)

    return data


@utils.check_company_existence
def get_balance_sheet(company: str, frequency: str = "annual") -> pd.DataFrame:
    """Get balance sheet data of a given symbol

    Args:
        company (str): Ticker symbol(e.g. 'IAM', 'MNG')
        frequency (str, optional): Display either quarter or annual data. Defaults to "annual".

    Raises:
        ValueError: frequency should be annual or quarter

    Returns:
        pd.DataFrame: Dataframe of balance sheet data
    """
    if frequency == "annual":
        url = (
            "https://www.marketwatch.com/investing/stock/"
            + company
            + "/financials/balance-sheet?countrycode=ma"
        )
        cols = ["Item Item", "5-year trend"]
    elif frequency == "quarter":
        url = (
            "https://www.marketwatch.com/investing/stock/"
            + company
            + "/financials/balance-sheet/quarter?countrycode=ma"
        )
        cols = ["Item Item", "5- qtr trend"]
    else:
        raise ValueError("frequency should be annual or quarter")

    request_data = utils.get_request(url)
    soup = BeautifulSoup(request_data.text, "lxml")

    data = soup.find_all(
        "table", {"class": "table table--overflow align--right"}
    )

    tab1 = pd.read_html(str(data))[0]
    tab2 = pd.read_html(str(data))[1]
    tab1["Item Item"] = tab1["Item Item"].apply(utils.remove_duplicates)
    tab2["Item Item"] = tab2["Item Item"].apply(utils.remove_duplicates)
    tab1.set_index(
        pd.MultiIndex.from_product(
            [["Assets"], tab1["Item Item"]], names=["", "Item"]
        ),
        inplace=True,
    )
    tab1.drop(cols, axis=1, inplace=True)
    tab2.set_index(
        pd.MultiIndex.from_product(
            [["Liabilities & Shareholders' Equity"], tab2["Item Item"]],
            names=["", "Item"],
        ),
        inplace=True,
    )
    tab2.drop(cols, axis=1, inplace=True)
    data = pd.concat([tab1, tab2], sort=True)

    return data


@utils.check_company_existence
def get_income_statement(
    company: str, frequency: str = "annual"
) -> pd.DataFrame:
    """Get income statement data of a given symbol

    Args:
        company (str): Ticker symbol(e.g. 'IAM', 'MNG')
        frequency (str, optional): Display either quarter or annual data. Defaults to "annual".
    Raises:
        ValueError: frequency should be annual or quarter

    Returns:
        pd.DataFrame: Dataframe of income statement data
    """
    if frequency == "annual":
        url = (
            "https://www.marketwatch.com/investing/stock/"
            + company
            + "/financials/income?countrycode=ma"
        )
        cols = ["5-year trend"]
    elif frequency == "quarter":
        url = (
            "https://www.marketwatch.com/investing/stock/"
            + company
            + "/financials/income/quarter?countrycode=ma"
        )
        cols = ["5- qtr trend"]
    else:
        raise ValueError("frequency should be annual or quarter")

    request_data = utils.get_request(url)
    soup = BeautifulSoup(request_data.text, "lxml")

    data = soup.find_all(
        "table", {"class": "table table--overflow align--right"}
    )

    data = pd.read_html(str(data))[0]
    data["Item Item"] = data["Item Item"].apply(utils.remove_duplicates)
    data.set_index("Item Item", inplace=True)
    data.drop(cols, axis=1, inplace=True)
    data.index.rename("Item", inplace=True)

    return data


@utils.check_company_existence
def get_cash_flow(company: str, frequency: str = "annual") -> pd.DataFrame:
    """Get cash flow data of a given symbol

    Args:
        company (str): Ticker symbol(e.g. 'IAM', 'MNG')
        frequency (str, optional): Display either quarter or annual data. Defaults to "annual".

    Raises:
        ValueError: frequency should be annual or quarter

    Returns:
        pd.DataFrame: Dataframe of cash flow data
    """
    if frequency == "annual":
        url = (
            "https://www.marketwatch.com/investing/stock/"
            + company
            + "/financials/cash-flow?countrycode=ma"
        )
        cols = ["Item Item", "5-year trend"]
    elif frequency == "quarter":
        url = (
            "https://www.marketwatch.com/investing/stock/"
            + company
            + "/financials/cash-flow/quarter?countrycode=ma"
        )
        cols = ["Item Item", "5- qtr trend"]
    else:
        raise ValueError("frequency should be annual or quarter")

    request_data = utils.get_request(url)
    soup = BeautifulSoup(request_data.text, "lxml")

    data = soup.find_all(
        "table", {"class": "table table--overflow align--right"}
    )
    data = pd.read_html(str(data))
    activ = [
        "Operating Activities",
        "Investing Activities",
        "Financing Activities",
    ]
    dataframes = []
    for i in range(3):
        tab = data[i]
        tab["Item Item"] = tab["Item Item"].apply(utils.remove_duplicates)
        tab.set_index(
            pd.MultiIndex.from_product(
                [[activ[i]], tab["Item Item"]], names=["", "Item"]
            ),
            inplace=True,
        )
        tab.drop(cols, axis=1, inplace=True)
        dataframes.append(tab)

    data = pd.concat(dataframes)

    return data


@utils.check_company_existence
def get_quote_table(company: str) -> pd.DataFrame:
    """Get important data about a given symbol

    Args:
        company (str): Ticker symbol(e.g. 'IAM', 'MNG')

    Returns:
        pd.DataFrame: Dataframe of data about the ticker
    """
    url = (
        f"https://www.marketwatch.com/investing/stock/{company}?countrycode=ma"
    )

    request_data = utils.get_request(url)
    soup = BeautifulSoup(request_data.text, "lxml")
    data = soup.find_all("li", {"class": "kv__item"})
    dataframe: Dict = {"Key Data": [], "Value": []}
    for li in data:
        dataframe["Key Data"].append(
            li.find("small", {"class": "label"}).contents[0]
        )
        content = li.find("span", {"class": "primary"})
        if content is None:
            dataframe["Value"].append(np.nan)
        else:
            dataframe["Value"].append(content.contents[0].replace("د.م.", ""))
    data = pd.DataFrame(dataframe)

    return data


def get_market_status() -> str:
    """Get status of the Moroccan market

    Returns:
        str: Status of the market(OPEN/CLOSED)
    """
    url = "https://www.marketwatch.com/investing/stock/iam?countryCode=ma"

    request_data = utils.get_request(url)
    soup = BeautifulSoup(request_data.text, "lxml")
    data = soup.find_all("div", {"class": "status"})
    data = data[0].contents[0]

    return data


@utils.check_company_existence
def get_company_officers(company: str) -> pd.DataFrame:
    """Get company officers(Names and roles) of a given symbol

    Args:
        company (str): Ticker symbol(e.g. 'IAM', 'MNG')

    Returns:
        pd.DataFrame: Dataframe of names and roles of the officers
    """
    url = (
        "https://www.wsj.com/market-data/quotes/MA/XCAS/"
        + company
        + "/company-people"
    )

    request_data = utils.get_request(url)
    soup = BeautifulSoup(request_data.text, "lxml")
    data = soup.find_all(
        "ul", {"class": "cr_data_collection cr_all_executives"}
    )
    dataframe: Dict = {"Name": [], "Role": []}
    for i in data:
        div = i.find_all("div", {"class": "cr_data_field"})
        for tag in div:
            dataframe["Name"].append(tag.find("a").contents[0])
            dataframe["Role"].append(
                tag.find("span", {"class": "data_lbl"}).contents[0]
            )
    data = pd.DataFrame(dataframe)

    return data


@utils.check_company_existence
def get_company_info(company: str) -> pd.DataFrame:
    """Get information related to the company's location, adresse...

    Args:
        company (str): Ticker symbol(e.g. 'IAM', 'MNG')

    Returns:
        pd.DataFrame: Dataframe of information related to the company (e.g. Name, Adresse, Phone...)
    """
    url = (
        "https://www.marketwatch.com/investing/stock/"
        + company
        + "/company-profile?countrycode=ma"
    )

    request_data = utils.get_request(url)
    soup = BeautifulSoup(request_data.text, "lxml")
    tmp = []
    tmp.append(soup.find("h4", {"class": "heading"}).contents[0])
    div_addr = soup.find_all("div", {"class": "address__line"})
    tmp.append(" ".join([x.contents[0] for x in div_addr]))
    tmp.append(
        "+"
        + soup.find("div", {"class": "phone"})
        .find("span", {"class": "text"})
        .contents[0]
    )
    div = soup.find_all("li", {"class": "kv__item w100"})
    tmp.append(div[0].find("span", {"class": "primary"}).contents[0])
    tmp.append(div[1].find("span", {"class": "primary"}).contents[0])
    tmp.append(soup.find("p", {"class": "description__text"}).contents[0])
    dataframe = {
        "Item": [
            "Name",
            "Address",
            "Phone",
            "Industry",
            "Sector",
            "Description",
        ],
        "Value": tmp,
    }
    return pd.DataFrame(dataframe)


def get_data_sectors() -> pd.DataFrame:
    """Get price data of sectors

    Returns:
        pd.DataFrame: Dataframe of price data of sectors
    """
    warnings.warn(
        "The function's proper operation may be impeded by specific runtime errors. Nevertheless, it is anticipated that this concern will be addressed in the forthcoming release.",
        RuntimeWarning,
    )

    url = "https://bourse.gbp.ma/bcp/indices"
    request_data = utils.get_request(url)
    soup = BeautifulSoup(request_data.text, "lxml")
    data = soup.find_all(
        "table",
        {
            "class": "table table-striped palmares table-condensed rwdTable streamingTable",
            "id": "table1",
        },
    )

    data = pd.read_html(str(data), thousands="'")[0]
    data.drop(["Kurs", "Var (%)"], axis=1, inplace=True)
    cols = ["Sector", "Date", "Close", "Open", "Low", "High"]
    data.columns = cols
    data.Date = pd.to_datetime(data.Date, format="%d.%m.%Y")

    return data


def get_sectors() -> None:
    """Show available sectors"""
    for sector in SECTORS.keys():
        print(sector)


@utils.check_sector_existence
def get_price_sector(
    sector: str, start_date: str, end_date: T_ed
) -> pd.DataFrame:
    """Get historical OHLC data for a given sector

    Args:
        sector (str): Sector name(e.g. 'BANQUES', 'boissons')
        start_date (str): (YYYY-MM-DD) Starting date to pull data from, limited to a maximum of five year
        end_date (T_ed): (YYYY-MM-DD) Ending date

    Returns:
        pd.DataFrame: Dataframe of historical OHLC data
    """
    warnings.warn(
        "The function's proper operation may be impeded by specific runtime errors. Nevertheless, it is anticipated that this concern will be addressed in the forthcoming release.",
        RuntimeWarning,
    )

    num_sector = SECTORS[sector]
    url = (
        "https://bourse.gbp.ma/bcp/api/series?lid="
        + num_sector
        + "&max=1250&mode=snap&period=1d&vt=yes"
    )

    request_data = utils.get_request(url)
    data_j = json.loads(request_data.content)
    data = pd.DataFrame(data_j["prices"])
    data.columns = ["Date", "Close", "High", "Low", "Open"]
    data.index = pd.to_datetime(
        data.Date.apply(lambda x: datetime.fromtimestamp(x / 1000.0).date())
    )
    data = data.loc[lambda x: (start_date <= x.index) & (x.index <= end_date)]
    data.set_index(
        pd.MultiIndex.from_product(
            [[data_j["name"]], data.index], names=["Sector", "Date"]
        ),
        inplace=True,
    )
    data.drop(["Date"], axis=1, inplace=True)

    return data


def get_data_sector(
    sectors: Union[str, List[str]],
    start_date: str,
    end_date: T_ed = datetime.now().strftime("%Y-%m-%d"),
) -> pd.DataFrame:
    """Get historical OHLC data for a given sector(s)

    Args:
        sectors (Union[str, List[str]]): List or str of sectors names(e.g. ['hotel', 'PETROLE ET GAZ'] or 'BANQUES')
        start_date (str): (YYYY-MM-DD) Starting date to pull data from, limited to a maximum of five years
        end_date (T_ed, optional): (YYYY-MM-DD) Ending date. Defaults to the current local date

    Raises:
        ValueError: end_date is greater than today's date
        ValueError: start_date is limited to a maximum of six year

    Returns:
        pd.DataFrame: Dataframe of historical OHLC data
    """
    warnings.warn(
        "The function's proper operation may be impeded by specific runtime errors. Nevertheless, it is anticipated that this concern will be addressed in the forthcoming release.",
        RuntimeWarning,
    )

    today: datetime = datetime.now()
    five_year_from_now: datetime = today - relativedelta(years=5)

    if datetime.strptime(end_date, "%Y-%m-%d") > today:
        raise ValueError(
            "end_date is greater than {today}".format(
                today=today.strftime("%Y-%m-%d")
            )
        )
    if datetime.strptime(start_date, "%Y-%m-%d") < five_year_from_now:
        raise ValueError("start_date is limited to a maximum of five year")

    if isinstance(sectors, list):
        dataframes: List = [
            get_price_sector(t, start_date, end_date) for t in sectors
        ]
        return pd.concat(dataframes, sort=True)
    else:
        return get_price_sector(sectors, start_date, end_date)


@utils.check_sector_existence
def get_sector_intraday(sector: str) -> pd.DataFrame:
    """Get intraday price data of a given sector

    Args:
        sector (str): Sector name(e.g. 'BANQUES', 'boissons')

    Returns:
        pd.DataFrame: Dataframe of intraday price data
    """
    warnings.warn(
        "The function's proper operation may be impeded by specific runtime errors. Nevertheless, it is anticipated that this concern will be addressed in the forthcoming release.",
        RuntimeWarning,
    )
    print(sector)
    num_sector = SECTORS[sector]
    url = (
        "https://bourse.gbp.ma/bcp/api/series/intraday?decorator=ajax&lid="
        + num_sector
        + "&mode=snap&period=1m&max=1254"
    )

    request_data = utils.get_request(url)
    data_j = json.loads(request_data.content)["data"]
    data = pd.DataFrame(data_j, columns=["Datetime", "Price"])
    data.index = pd.to_datetime(
        data.Datetime.apply(lambda x: datetime.fromtimestamp(x / 1000.0))
    )

    data.drop("Datetime", axis=1, inplace=True)

    return data


def get_best_performers() -> pd.DataFrame:
    """Get best performers for a given session

    Returns:
        pd.DataFrame: Dataframe of the best performing indices, their current price, and their variation
    """

    url = (
        "https://medias24.com/content/api?method=getBestPerformers&format=json"
    )
    request_data = utils.get_request(url)

    data_j = json.loads(request_data.content)["result"]
    data = pd.DataFrame(data_j)
    data.columns = ["Name", "Price", "Variation"]

    return data


def get_worst_performers() -> pd.DataFrame:
    """Get worst performers for a given session

    Returns:
        pd.DataFrame: Dataframe of the worst performing indices, their current price, and their variation
    """
    url = "https://medias24.com/content/api?method=getWorstPerformers&format=json"
    request_data = utils.get_request(url)

    data_j = json.loads(request_data.content)["result"]
    data = pd.DataFrame(data_j)
    data.columns = ["Name", "Price", "Variation"]

    return data
