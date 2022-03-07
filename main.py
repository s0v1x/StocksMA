import requests
from bs4 import BeautifulSoup 
import pandas as pd
from io import StringIO
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def get_data(ticker, start_date, end_date):

  today = datetime.now()
  one_year_from_now = today - relativedelta(years=1)

  if datetime.strptime(end_date, "%m/%d/%Y") > today:
    raise ValueError("end_date is greater than {today}".format(today=today.strftime('%m/%d/%Y')))
  if datetime.strptime(start_date, "%m/%d/%Y") < one_year_from_now:
    raise ValueError("start_date is limited to a maximum of one year")

  url = 'https://www.marketwatch.com/investing/stock/{ticker}/download-data?startDate={s_date}&endDate={e_date}&countryCode=ma'.format(ticker=ticker,
                                                                                                                                       s_date=start_date,
                                                                                                                                       e_date=end_date)
  
  r = requests.get(url)
  soup = BeautifulSoup(r.content, "html.parser")
  url_data = soup.find("a", class_="link link--csv m100")['href']
  data = requests.get(url_data)
  df = pd.read_csv(StringIO(data.text), sep=",", index_col=[0])
  df = df[end_date : start_date]
  for cl in df.columns:
    df[cl] = df[cl].apply(convert_obj)

  return df