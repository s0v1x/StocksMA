import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils import convert_obj

companies = {'ADH': 'Addoha',
 'ADI': 'Alliances',
 'AFI': 'Afric Indus.',
 'AFM': 'AFMA',
 'AGM': 'Agma',
 'ALM': 'Aluminium Maroc',
 'ARD': 'Aradei Capital',
 'ATH': 'AutoHall',
 'ATL': 'ATLANTASANAD',
 'ATW': 'AttijariwafaBk',
 'BAL': 'BALIMA',
 'BCI': 'BMCI',
 'BCP': 'BCP',
 'BOA': 'BANK OF AFRICA',
 'CDA': 'Central Danone',
 'CDM': 'CDM',
 'CIH': 'CIH',
 'CMA': 'Ciments Maroc',
 'CMT': 'CMT',
 'COL': 'Colorado',
 'CRS': 'Cartier Saada',
 'CSR': 'COSUMAR',
 'CTM': 'CTM',
 'DHO': 'DeltaHolding',
 'DIS': 'DiacSalaf',
 'DLM': 'DelattreLev.',
 'DRI': 'Dari Couspate',
 'DWY': 'DISWAY',
 'EQD': 'EQDOM',
 'FBR': 'FENIE BROSSETTE',
 'GAZ': 'Afriquia Gaz',
 'HPS': 'HPS',
 'IAM': 'Maroc Telecom',
 'IBC': 'IBMaroc.com',
 'IMO': 'Immr Invest Br',
 'INV': 'INVOLYS',
 'JET': 'Jet Contractors',
 'LBV': 'LABEL VIE',
 'LES': 'Lesieur Cristal',
 'LHM': 'Lafarge Holcim',
 'LYD': 'Lydec',
 'M2M': 'M2M Group',
 'MAB': 'Maghrebail',
 'MDP': 'MED PAPER',
 'MIC': 'MICRODATA',
 'MLE': 'Maroc Leasing',
 'MNG': 'Managem',
 'MOX': 'Maghreb Oxygene',
 'MSA': 'SODEP-MarsaMaroc',
 'MUT': 'MUTANDIS',
 'NEJ': 'Auto Nejma',
 'NEX': 'Nexans Maroc',
 'NKL': 'EnnaklN',
 'OUL': 'Oulmes',
 'PRO': 'PROMOPHARM',
 'RDS': 'Res. Dar Saada',
 'REB': 'Rebab Company',
 'RIS': 'Risma',
 'S2M': 'S2M',
 'SAH': 'Saham Assurance',
 'SAM': 'SAMIR',
 'SBM': 'Stokvis Nord Afr.',
 'SID': 'Sonasid',
 'SLF': 'SALAFIN',
 'SMI': 'SMI',
 'SNA': 'SNEP',
 'SNP': 'REALISATIONS MECANIQUES',
 'SOT': 'SOTHEMA',
 'SRM': 'Ste Boissons Maroc',
 'STR': 'STROC Indus.',
 'TIM': 'Timar',
 'TMA': 'TotalMaroc',
 'TQM': 'TAQA Morocco',
 'UMR': 'Unimer',
 'WAA': 'WAFA ASSURANCE'}


def get_isin(company):
  url = "https://www.leboursier.ma/api?method=searchStock&format=json&search="+str(company)
  r = requests.get(url)
  #r.encoding='utf-8-sig'
  result = json.loads(r.content)['result']
  l_result = len(result)
  if l_result == 0:
    raise ValueError("Company {company} cannot be found".format(company=str(company)))
  elif l_result > 1:
    names = [n['name'] for n in result]
    raise Exception("Found severale companies with the same name {company} \n {res}".format(company='llll', res=names))
  else :
    return result[0]['name'],result[0]['isin']
    
def get_tickers():
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
  df.set_index(pd.MultiIndex.from_product([[ticker], df.index], names=['Symbol', 'Date']), inplace=True)

  return df


def get_data(tickers, start_date, end_date=datetime.now()):

    today = datetime.now()
    one_year_from_now = today - relativedelta(years=1)

    if datetime.strptime(end_date, "%m/%d/%Y") > today:
        raise ValueError(
            "end_date is greater than {today}".format(today=today.strftime("%m/%d/%Y"))
        )
    if datetime.strptime(start_date, "%m/%d/%Y") < one_year_from_now:
        raise ValueError("start_date is limited to a maximum of one year")

    if isinstance(tickers, list):
      tickers = [x.upper() for x in tickers]
      dataframes = []
      for t in tickers:
        if t in companies:
          dataframes.append(get_data_ticker(t, start_date, end_date))
        else:
          raise ValueError("Ticker {ticker} is unknown".format(ticker=t))
      df = pd.concat(dataframes, sort=True)
      return df
    
    else:
      tickers = tickers.upper()
      if tickers in companies:
        return get_data_ticker(tickers, start_date, end_date)
      else:
        raise ValueError("Ticker {ticker} is unknown".format(ticker=tickers))

