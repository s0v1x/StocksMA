import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

r = requests.get('https://www.marketwatch.com/investing/stock/dwy/download-data?countrycode=ma')
soup = BeautifulSoup(r.content, "html.parser")



data = soup.find("a", class_="link link--csv m100")['href']
rr = requests.get(data)

print(pd.read_csv(StringIO(rr.text), sep=","))