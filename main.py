import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils import convert_obj


def get_tickers():
    companies = {
        "Addoha": "ADH",
        "AFMA": "AFM",
        "Afric Indus.": "AFI",
        "Afriquia Gaz": "GAZ",
        "Agma": "AGM",
        "Alliances": "ADI",
        "Aluminium Maroc": "ALM",
        "Aradei Capital": "ARD",
        "ATLANTASANAD": "ATL",
        "AttijariwafaBk": "ATW",
        "AutoHall": "ATH",
        "Auto Nejma": "NEJ",
        "BALIMA": "BAL",
        "BANK OF AFRICA": "BOA",
        "BCP": "BCP",
        "BMCI": "BCI",
        "Cartier Saada": "CRS",
        "CDM": "CDM",
        "Central Danone": "CDA",
        "CIH": "CIH",
        "Ciments Maroc": "CMA",
        "CMT": "CMT",
        "Colorado": "COL",
        "COSUMAR": "CSR",
        "CTM": "CTM",
        "Dari Couspate": "DRI",
        "DelattreLev.": "DLM",
        "DeltaHolding": "DHO",
        "DiacSalaf": "DIS",
        "DISWAY": "DWY",
        "EnnaklN": "NKL",
        "EQDOM": "EQD",
        "FENIE BROSSETTE": "FBR",
        "HPS": "HPS",
        "IBMaroc.com": "IBC",
        "Immr Invest Br": "IMO",
        "INVOLYS": "INV",
        "Jet Contractors": "JET",
        "LABEL VIE": "LBV",
        "Lafarge Holcim": "LHM",
        "Lesieur Cristal": "LES",
        "Lydec": "LYD",
        "M2M Group": "M2M",
        "Maghreb Oxygene": "MOX",
        "Maghrebail": "MAB",
        "Managem": "MNG",
        "Maroc Leasing": "MLE",
        "Maroc Telecom": "IAM",
        "MED PAPER": "MDP",
        "MICRODATA": "MIC",
        "MUTANDIS": "MUT",
        "Nexans Maroc": "NEX",
        "Oulmes": "OUL",
        "PROMOPHARM": "PRO",
        "Rebab Company": "REB",
        "Res. Dar Saada": "RDS",
        "Risma": "RISMA",
        "S2M": "S2M",
        "Saham Assurance": "SAH",
        "SALAFIN": "SLF",
        "SAMIR": "SAM",
        "SMI": "SMI",
        "SNEP": "SNA",
        "REALISATIONS MECANIQUES": "SNP",
        "SODEP-MarsaMaroc": "MSA",
        "Sonasid": "SID",
        "SOTHEMA": "SOT",
        "Ste Boissons Maroc": "SRM",
        "Stokvis Nord Afr.": "SBM",
        "STROC Indus.": "STR",
        "TAQA Morocco": "TQM",
        "Timar": "TIM",
        "TotalMaroc": "TMA",
        "Unimer": "UMR",
        "WAFA ASSURANCE": "WAA",
        "Zellidja": "ZDJ",
    }
    for c in companies:
        print(c, '/', companies[c])

today = datetime.now()
one_year_from_now = today - relativedelta(years=1)

def get_data_ticker(ticker, start_date, end_date):
  url = "https://www.marketwatch.com/investing/stock/{ticker}/download-data?startDate={s_date}&endDate={e_date}&countryCode=ma".format(
        ticker=ticker, s_date=start_date, e_date=end_date
  )
  r = requests.get(url)
  soup = BeautifulSoup(r.content, "html.parser")
  url_data = soup.find("a", class_="link link--csv m100")["href"]
  data = requests.get(url_data)
  df = pd.read_csv(StringIO(data.text), sep=",", index_col=[0])
  df = df[end_date:start_date]
  for cl in df.columns:
      df[cl] = df[cl].apply(convert_obj)
  df.set_index(pd.MultiIndex.from_product([[ticker.upper()], df.index], names=['Symbol', 'Date']), inplace=True)

  return df

def get_data(tickers, start_date=one_year_from_now, end_date=today):

    if datetime.strptime(end_date, "%m/%d/%Y") > today:
        raise ValueError(
            "end_date is greater than {today}".format(today=today.strftime("%m/%d/%Y"))
        )
    if datetime.strptime(start_date, "%m/%d/%Y") < one_year_from_now:
        raise ValueError("start_date is limited to a maximum of one year")

    if isinstance(tickers, list):
      dataframes = []
      for t in tickers:
        dataframes.append(get_data_ticker(t, start_date, end_date))
      df = pd.concat(dataframes, sort=True)
      return df
    
    else:
      return get_data_ticker(tickers, start_date, end_date)
