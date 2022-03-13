import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils
import json

companies = {
    "ADH": "Douja Promotion Groupe Addoha",
    "ADI": "Alliances Developpement Immobilier S.A.",
    "AFI": "Afric Industries S.A.",
    "AFM": "AFMA S.A.",
    "AGM": "Agma S.A.",
    "ALM": "Aluminium du Maroc",
    "ARD": "Aradei Capital",
    "ATH": "Auto Hall S.A.",
    "ATL": "AtlantaSanad",
    "ATW": "Attijariwafa Bank",
    "BAL": "Societe Immobiliere Balima",
    "BCI": "Banque Marocaine pour le Commerce et l'Industrie ",
    "BCP": "Banque Centrale Populaire S.A.",
    "BOA": "Bank of Africa",
    "CDA": "Centrale Danone",
    "CDM": "Credit du Maroc",
    "CIH": "Credit Immobilier et Hotelier",
    "CMA": "Les Ciments du Maroc",
    "CMT": "Compagnie Miniere de Touissit S.A.",
    "COL": "Colorado S.A.",
    "CRS": "Cartier Saada S.A.",
    "CSR": "Cosumar",
    "CTM": "Compagnie de Transports au Maroc S.A.",
    "DHO": "Delta Holding S.A.",
    "DLM": "Delattre Levivier Maroc S.A.",
    "DWY": "Disway S.A.",
    "EQD": "Societe d'Equipement Domestique et Menager S.A. ",
    "FBR": "Fenie Brossette S.A.",
    "GAZ": "Afriquia Gaz",
    "HPS": "Hightech Payment Systems S.A.",
    "IAM": "Maroc Telecom",
    "IBC": "IB Maroc.com S.A.",
    "IMO": "Immorente Invest S.A.",
    "INV": "Involys",
    "JET": "Jet Contractors S.A.",
    "LBV": "Label Vie",
    "LES": "Lesieur Cristal S.A.",
    "LHM": "LafargeHolcim Maroc",
    "M2M": "m2m group S.A.",
    "MAB": "Maghrebail",
    "MDP": "Med Paper S.A.",
    "MIC": "Microdata S.A.R.L.",
    "MLE": "Maroc Leasing S.A.",
    "MNG": "Managem",
    "MOX": "Maghreb Oxygene",
    "MSA": "SODEP-Marsa Maroc",
    "MUT": "Mutandis SCA",
    "NEJ": "Auto Nejma Maroc S.A.",
    "NKL": "Ennakl Automobiles",
    "PRO": "Promopharm S.A.",
    "RDS": "Residences Dar Saada S.A.",
    "RIS": "Risma",
    "S2M": "Societe Maghrebine de Monetique",
    "SAH": "Saham Assurance S.A.",
    "SBM": "Societe des Boissons du Maroc",
    "SID": "Societe Nationale de Siderurgie S.A.",
    "SLF": "Salafin",
    "SMI": "Societe Metallurgique d'Imiter ",
    "SNA": "Stokvis Nord Afrique",
    "SNP": "Societe Nationale d'Electrolyse et de Petrochimie ",
    "SOT": "Sothema",
    "SRM": "Societe de Realisations Mecaniques",
    "STR": "STROC Industrie S.A.",
    "TGC": "Travaux Generaux de Construction de Casablanca S.A.",
    "TIM": "TIMAR S.A.",
    "TMA": "TotalEnergies Marketing Maroc",
    "TQM": "Taqa Morocco",
    "WAA": "Wafa Assurance S.A.",
    "ZDJ": "Zellidja S.A.",
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
