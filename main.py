import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils
import json


today = datetime.now()
one_year_from_now = today - relativedelta(years=1)


def get_tickers():
    for c in utils.companies:
        print(c, "/", utils.companies[c])


def get_isin(company):
    if not str(company):
        raise Exception("Company must be defined not empty")

    url = "https://www.leboursier.ma/api?method=searchStock&format=json&search=" + str(
        company
    )
    headers = {"User-Agent": utils.rand_agent("user-agents.txt")}
    r = requests.get(url, headers=headers)
    # r.encoding='utf-8-sig'
    result = json.loads(r.content)["result"]
    l_result = len(result)

    if l_result == 0:
        if company.upper() in utils.companies.keys():
            return get_isin(utils.companies[company.upper()])
        else:
            raise Exception(
                "Company {company} cannot be found".format(company=str(company))
            )

    elif l_result > 1:
        names = [n["name"] for n in result]
        if company in names:
            return result[0]["name"], result[0]["isin"]
        else:
            raise Exception(
                "Found severale utils.companies with the same name {company} \n {res}".format(
                    company=company, res=names
                )
            )
    else:
        return result[0]["name"], result[0]["isin"]


def get_data_stock(company, start_date, end_date):

    _NAME, _ISIN = get_isin(str(company))
    url = (
        "https://www.leboursier.ma/api?method=getStockOHLC&ISIN="
        + _ISIN
        + "&format=json"
    )
    headers = {"User-Agent": utils.rand_agent("user-agents.txt")}
    request_data = requests.get(url, headers=headers)
    data = json.loads(request_data.content)
    data = pd.DataFrame(
        data["result"], columns=["Date", "Open", "High", "Low", "Close", "Volume"]
    )
    data.index = pd.to_datetime(
        data.Date.apply(lambda x: datetime.fromtimestamp(x / 1000.0).date())
    )
    data = data[start_date:end_date]
    data.set_index(
        pd.MultiIndex.from_product([[_NAME], data.index], names=["Company", "Date"]),
        inplace=True,
    )
    data.drop(["Date"], axis=1, inplace=True)

    return data


def get_data(tickers, start_date, end_date=datetime.now()):

    today = datetime.now()
    one_year_from_now = today - relativedelta(years=6)

    if datetime.strptime(end_date, "%Y-%m-%d") > today:
        raise Exception(
            "end_date is greater than {today}".format(today=today.strftime("%Y-%m-%d"))
        )
    if datetime.strptime(start_date, "%Y-%m-%d") < one_year_from_now:
        raise Exception("start_date is limited to a maximum of six year")

    if isinstance(tickers, list):
        dataframes = []
        for t in tickers:
            dataframes.append(get_data_stock(t, start_date, end_date))
        df = pd.concat(dataframes, sort=True)
        return df
    else:
        return get_data_stock(tickers, start_date, end_date)


def get_info(company):
    _NAME, _ISIN = get_isin(str(company))
    url = (
        "https://www.leboursier.ma/api?method=getStockInfo&ISIN="
        + _ISIN
        + "&format=json"
    )
    headers = {"User-Agent": utils.rand_agent("user-agents.txt")}

    request_data = requests.get(url, headers=headers)
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


def get_data_intraday(company):

    _NAME, _ISIN = get_isin(str(company))
    _DATE = (
        get_info(_ISIN)["Quotation Datetime"].to_string(index=False).replace("à", "")
    )
    url = (
        "https://www.leboursier.ma/api?method=getStockIntraday&ISIN="
        + _ISIN
        + "&format=json"
    )
    headers = {"User-Agent": utils.rand_agent("user-agents.txt")}
    request_data = requests.get(url, headers=headers)
    data = json.loads(request_data.content)["result"][0]
    data = pd.DataFrame(data)
    data.index = pd.to_datetime(
        data.labels.apply(
            lambda x: datetime.combine(
                datetime.strptime(_DATE, "%d/%m/%Y  %H:%M").date(),
                datetime.strptime(x, "%H:%M").time(),
            )
        )
    ).rename("Datetime")
    data.drop("labels", axis=1, inplace=True)

    return data
