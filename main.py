import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils
import json

companies = {
    "ADH": "Addoha",
    "ADI": "Alliances",
    "AFI": "Afric Indus.",
    "AFM": "AFMA",
    "AGM": "Agma",
    "ALM": "Aluminium Maroc",
    "ARD": "Aradei Capital",
    "ATH": "AutoHall",
    "ATL": "ATLANTASANAD",
    "ATW": "AttijariwafaBk",
    "BAL": "BALIMA",
    "BCI": "BMCI",
    "BCP": "BCP",
    "BOA": "BANK OF AFRICA",
    "CDA": "Central Danone",
    "CDM": "CDM",
    "CIH": "CIH",
    "CMA": "Ciments Maroc",
    "CMT": "CMT",
    "COL": "Colorado",
    "CRS": "Cartier Saada",
    "CSR": "COSUMAR",
    "CTM": "CTM",
    "DHO": "DeltaHolding",
    "DIS": "DiacSalaf",
    "DLM": "DelattreLev.",
    "DRI": "Dari Couspate",
    "DWY": "DISWAY",
    "EQD": "EQDOM",
    "FBR": "FENIE BROSSETTE",
    "GAZ": "Afriquia Gaz",
    "HPS": "HPS",
    "IAM": "Maroc Telecom",
    "IBC": "IBMaroc.com",
    "IMO": "Immr Invest Br",
    "INV": "INVOLYS",
    "JET": "Jet Contractors",
    "LBV": "LABEL VIE",
    "LES": "Lesieur Cristal",
    "LHM": "Lafarge Holcim",
    "LYD": "Lydec",
    "M2M": "M2M Group",
    "MAB": "Maghrebail",
    "MDP": "MED PAPER",
    "MIC": "MICRODATA",
    "MLE": "Maroc Leasing",
    "MNG": "Managem",
    "MOX": "Maghreb Oxygene",
    "MSA": "SODEP-MarsaMaroc",
    "MUT": "MUTANDIS",
    "NEJ": "Auto Nejma",
    "NEX": "Nexans Maroc",
    "NKL": "EnnaklN",
    "OUL": "Oulmes",
    "PRO": "PROMOPHARM",
    "RDS": "Res. Dar Saada",
    "REB": "Rebab Company",
    "RIS": "Risma",
    "S2M": "S2M",
    "SAH": "Saham Assurance",
    "SAM": "SAMIR",
    "SBM": "Stokvis Nord Afr.",
    "SID": "Sonasid",
    "SLF": "SALAFIN",
    "SMI": "SMI",
    "SNA": "SNEP",
    "SNP": "REALISATIONS MECANIQUES",
    "SOT": "SOTHEMA",
    "SRM": "Ste Boissons Maroc",
    "STR": "STROC Indus.",
    "TIM": "Timar",
    "TMA": "TotalMaroc",
    "TQM": "TAQA Morocco",
    "UMR": "Unimer",
    "WAA": "WAFA ASSURANCE",
}

today = datetime.now()
one_year_from_now = today - relativedelta(years=1)


def get_tickers():
    for c in companies:
        print(c, "/", companies[c])


def get_isin(company):
    if not company:
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
        raise Exception(
            "Company {company} cannot be found".format(company=str(company))
        )
    elif l_result > 1:
        names = [n["name"] for n in result]
        if company in names:
            return result[0]["name"], result[0]["isin"]
        else:
            raise Exception(
                "Found severale companies with the same name {company} \n {res}".format(
                    company=company, res=names
                )
            )
    else:
        return result[0]["name"], result[0]["isin"]


def get_data_stock(ticker, start_date, end_date):

    _NAME, _ISIN = get_isin(str(ticker))
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
