<div align="center">
  <p>
      <a href="https://pypi.org/project/StocksMA/"><img width="500" src="https://i.ibb.co/D73mr0j/stocks.png" alt="StocksMA" onerror="this.onerror=null;this.src='stocks.png';"/></a>
  </p>
  <b>Creating easier access to the Moroccan stock market data</b>
  
  <br />
</div>

---

<div align="center">

[![Language](https://img.shields.io/badge/Language-Python-green?style)](https://github.com/s0v1x)
[![PyPI](https://img.shields.io/pypi/v/StocksMA)](https://pypi.org/project/StocksMA/)
[![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flatcolor=BC4E99)](https://github.com/s0v1x/StocksMA)
[![GitHub license](https://img.shields.io/github/license/s0v1x/StocksMA)](https://github.com/s0v1x/StocksMA/blob/master/LICENSE)
[![Check Code](https://github.com/s0v1x/StocksMA/actions/workflows/check_code.yml/badge.svg)](https://github.com/s0v1x/StocksMA/actions/workflows/check_code.yml)

</div>

## What is StocksMA ?

StocksMA is a package to facilitate access to financial and economic data of Moroccan stocks. It tries to cover potentially valuable and interesting data points.

The package include functions to extract price data from [Leboursier](https://www.leboursier.ma/), financial ratios(income statement, balance sheet, cash flow) from [MarketWatch](https://www.marketwatch.com/), and profile data from [WSJ](https://www.wsj.com)

> Note: Sometimes, some functions may fail to get the data from some sources due to WAF protection.

## Installation

Python3 is required.

```bash
$ pip install StocksMA
```

## Usage

  - [Import the package](#import-the-package)
  - [Get all availabale tickers](#get-all-availabale-tickers)
  - [Get price data](#get-price-data)
    - [Get price data of multiple companies](#get-price-data)
    - [Get price data of single company](#get-price-data)
  - [Get session information](#get-session-information)
  - [Get intraday price data](#get-intraday-price-data)
  - [Get Ask Bid data](#get-ask-bid-data)
  - [Get balance sheet](#get-balance-sheet)
    - [Annual balance sheet](#get-balance-sheet)
    - [Quarter balance sheet](#get-balance-sheet)
  - [Get income statement](#get-income-statement)
    - [Annual income statement](#get-income-statement)
    - [Quarter income statement](#get-income-statement)
  - [Get cash flow](#get-cash-flow)
    - [Annual cash flow](#get-cash-flow)
    - [Quarter cash flow](#get-cash-flow)
  - [Get quote table](#get-quote-table)
  - [Get market status](#get-market-status)
  - [Get company officers](#get-company-officers)
  - [Get company information](#get-company-information)
  
### Import the package

```python
>> import StocksMA as stm
```

### Get all availabale tickers
Show available tickers with the full name of the company
**Example**:
```python
stm.get_tickers()
```

```bash
ADH / Douja Promotion Groupe Addoha
ADI / Alliances Developpement Immobilier S.A.
AFI / Afric Industries S.A.
AFM / AFMA S.A.
.
.
.
WAA / Wafa Assurance S.A.
ZDJ / Zellidja S.A.
```

<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get price data 
Get historical OHLCV data for a given symbol(s)

**Args**:
- **`tickers`** `Union[str, List[str]]` : List or str of companies names or ticker symbols(e.g. ['maroc telecom', 'MNG'] or 'CIH')
- **`start_date`** `str`: `(YYYY-MM-DD)` Starting date to pull data from, limited to a maximum of six year
- **`end_date`** `str`: `(YYYY-MM-DD)` Ending date. Defaults to the current local date

**Returns**:
- **`pd.DataFrame`**: Dataframe of historical OHLCV data

**Example**:
```python
# Get price data of multiple companies
stm.get_price_data(['CIH','maroc telecom', 'involys'], start_date='2020-11-14', end_date='2022-02-14')
```

|           	|            	| Close  	| High   	| Low    	| Open   	| Volume 	|
|-----------	|------------	|--------	|--------	|--------	|--------	|--------	|
| **Company** | **Date**    |        	|        	|        	|        	|        	|
| CIH P     	| 2020-11-16 	| 248.15 	| 248.15 	| 248.00 	| 248.00 	| 8      	|
|           	| 2020-11-17 	| 250.00 	| 250.00 	| 248.00 	| 248.10 	| 220    	|
|           	| 2020-11-19 	| 245.20 	| 248.00 	| 245.10 	| 248.00 	| 133    	|
|           	| ...        	| ...    	| ...    	| ...    	| ...    	| ...    	|
| INVOLYS P 	| 2022-02-08 	| 131.95 	| 131.95 	| 131.95 	| 131.95 	| 5      	|
|           	| 2022-02-09 	| 131.95 	| 131.95 	| 131.90 	| 131.95 	| 100    	|
|           	| 2022-02-11 	| 131.90 	| 131.90 	| 131.00 	| 131.00 	| 4      	|

[840 rows x 5 columns]


```python
# Get price data of single company
stm.get_price_data('involys', start_date='2020-11-14', end_date='2022-02-14')
```

|           	|            	| Open   	| High   	| Low    	| Close  	| Volume 	|
|-----------	|------------	|--------	|--------	|--------	|--------	|--------	|
| **Company**   | **Date**      |        	|        	|        	|        	|        	|
| INVOLYS P 	| 2020-11-16 	| 119.50 	| 121.00 	| 119.50 	| 121.00 	| 11     	|
|           	| 2020-11-17 	| 118.60 	| 121.00 	| 118.60 	| 121.00 	| 22     	|
|           	| 2020-11-19 	| 121.00 	| 121.00 	| 121.00 	| 121.00 	| 1      	|
|           	| ...        	| ...    	| ...    	| ...    	| ...    	| ...    	|
|           	| 2022-02-09 	| 131.95 	| 131.95 	| 131.90 	| 131.95 	| 100    	|
|           	| 2022-02-11 	| 131.00 	| 131.90 	| 131.00 	| 131.90 	| 4      	|

[253 rows x 5 columns]


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get session information
Get data related to the current trading session of a given symbol

**Args**:
- **`company`** `str`: Company name or ticker symbol(e.g. 'maroc telecom', 'MNG')

**Returns**:
- **`pd.DataFrame`**: Dataframe of session data

**Example**:
```python
stm.get_session_info('involys')
```

|   	| Name      	| Name_2  	| ISIN         	| Number of Shares 	| Close   	| Previous Close 	| Market Cap  	| Quotation Datetime 	|  Change Volume 	| Change 	| Volume in Shares 	| Volume 	| Open    	| Low     	| High    	|
|---	|-----------	|---------	|--------------	|------------------	|---------	|----------------	|-------------	|--------------------	|----------------	|--------	|------------------	|--------	|---------	|---------	|---------	|
| 1 	| INVOLYS P 	| INVOLYS 	| MA0000011579 	| 382716           	| 109.950 	| 109.95         	| 42079624.20 	| 18/03/2022 à 15:16 	| 0.00           	| 0.00   	| 5387             	| 49     	| 109.400 	| 109.400 	| 109.950 	|


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get intraday price data
Get intraday price data of a given symbol

**Args**:
- **`company`** `str`: Company name or ticker symbol(e.g. 'maroc telecom', 'MNG')

**Returns**:
- **`pd.DataFrame`**: Dataframe of intraday price data

**Example:**
```python
stm.get_data_intraday('CIH')
```

|                     	| prices 	|
|---------------------	|--------	|
| **Datetime**          |        	|
| 2022-03-18 09:30:00 	| 130.20 	|
| 2022-03-18 10:02:00 	| 131.00 	|
| 2022-03-18 10:06:00 	| 131.00 	|
| 2022-03-18 10:07:00 	| 131.00 	|
| 2022-03-18 10:17:00 	| 131.15 	|
| 2022-03-18 10:24:00 	| 131.15 	|
| 2022-03-18 10:30:00 	| 131.15 	|
| 2022-03-18 10:41:00 	| 131.40 	|
| 2022-03-18 11:07:00 	| 131.40 	|
| 2022-03-18 11:15:00 	| 131.40 	|
| 2022-03-18 12:24:00 	| 131.45 	|
| 2022-03-18 12:31:00 	| 131.40 	|
| 2022-03-18 13:25:00 	| 131.20 	|
| 2022-03-18 14:48:00 	| 131.25 	|
| 2022-03-18 15:07:00 	| 131.40 	|
| 2022-03-18 15:19:00 	| 131.25 	|
| 2022-03-18 15:30:00 	| 131.40 	|


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get Ask Bid data
Get ask bid data of a given symbol

**Args**:
- **`company`** `str`: Company name or ticker symbol(e.g. 'maroc telecom', 'MNG')

**Returns**:
- **`pd.DataFrame`**: Dataframe of ask bid data

**Example:**
```python
stm.get_ask_bid('CIH')
```

|   	| bidValue 	| bidQte 	| askValue 	| askQte 	| bidOrder 	| askOrder 	|
|---	|----------	|--------	|----------	|--------	|----------	|----------	|
| 0 	| 340.1    	| 3      	| 350.0    	| 248    	| 1        	| 2        	|
| 1 	| 340.0    	| 950    	| 352.0    	| 702    	| 2        	| 1        	|
| 2 	| 337.1    	| 4      	| 354.5    	| 10     	| 1        	| 1        	|
| 3 	| 336.2    	| 10     	| 354.9    	| 3      	| 1        	| 1        	|
| 4 	| 335.0    	| 10     	| 355.0    	| 290    	| 1        	| 2        	|
| 5 	| 334.0    	| 4      	| 356.0    	| 200    	| 1        	| 2        	|
| 6 	| 332.0    	| 6      	| 357.9    	| 2      	| 2        	| 1        	|
| 7 	| 330.5    	| 10     	| 358.0    	| 482    	| 1        	| 2        	|
| 8 	| 330.0    	| 274    	| 359.0    	| 59     	| 3        	| 1        	|
| 9 	| 321.5    	| 300    	| 359.4    	| 20     	| 1        	| 1        	|


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get balance sheet
Get balance sheet data of a given symbol

**Args**:
- **`company`** `str`: Ticker symbol(e.g. 'IAM', 'MNG')
- **`frequency`** `str`: Display either quarter or annual data. Defaults to "annual".

**Returns**:
- **`pd.DataFrame`**: Dataframe of balance sheet data

**Example:**
```python
# Annual balance sheet
stm.get_balance_sheet('ATW', frequency='annual')
```

|                                    	|                                     	| 2017   	| 2018    	| 2019    	| 2020    	| 2021      |
|------------------------------------	|-------------------------------------	|---------	|---------	|---------	|---------	|---------	|
|                                    	| **Item**                              |         	|         	|         	|         	|         	|
| Assets                             	| Total Cash & Due from Banks         	| 18.22B  	| 18.54B  	| 24.73B  	| 26.33B  	| 25.74B  	|
|                                    	| Cash & Due from Banks Growth        	| -       	| 1.71%   	| 33.42%  	| 6.48%   	| -2.26%  	|
|                                    	| Investments - Total                 	| 116.38B 	| 119.86B 	| 123.75B 	| 137.55B 	| 158.73B 	|
|                                    	| Investments Growth                  	| -       	| 2.99%   	| 3.25%   	| 11.15%  	| 15.40%  	|
|                                    	| Trading Account Securities          	| -       	| -       	| 54.32B  	| 58.67B  	| 69.91B  	|
|                                    	| ...                                 	| ...     	| ...     	| ...     	| ...     	| ...     	|
| Liabilities & Shareholders' Equity 	| Total Shareholders' Equity / Assets 	| 8.40%   	| 8.73%   	| 8.94%   	| 8.41%   	| 8.80%   	|
|                                    	| Return On Average Total Equity      	| -       	| -       	| -       	| -       	| 10.26%  	|
|                                    	| Accumulated Minority Interest       	| 6.44B   	| 5.95B   	| 6.3B    	| 6.49B   	| 7.34B   	|
|                                    	| Total Equity                        	| 46.06B  	| 50.47B  	| 53.93B  	| 54.29B  	| 59.79B  	|
|                                    	| Liabilities & Shareholders' Equity  	| 471.47B 	| 509.93B 	| 532.6B  	| 568.11B 	| 596.33B 	|

[74 rows x 5 columns]


```python
# Quarter balance sheet
stm.get_balance_sheet('ATW', frequency='quarter')
```

|                                     	|                                     	| 30-Jun-2021 	| 30-Sep-2021 	| 31-Dec-2020 	| 31-Dec-2021 	| 31-Mar-2021 	|
|-------------------------------------	|-------------------------------------	|-------------	|-------------	|-------------	|-------------	|-------------	|
|                                     	| **Item**                                	|             	|             	|             	|             	|             	|
| Assets                              	| Total Cash & Due from Banks         	| 23.41B      	| 20.2B       	| 26.33B      	| 25.74B      	| 22.79B      	|
|                                     	| Cash & Due from Banks Growth        	| 2.74%       	| -13.73%     	| -           	| 27.43%      	| -13.47%     	|
|                                     	| Investments - Total                 	| 148.98B     	| 155.57B     	| 137.55B     	| 158.73B     	| 141.76B     	|
|                                     	| Investments Growth                  	| 5.10%       	| 4.42%       	| -           	| 2.04%       	| 3.06%       	|
|                                     	| Trading Account Securities          	| 63.98B      	| 64.94B      	| 58.67B      	| 69.91B      	| 61.8B       	|
|                                     	| ...                                 	| ...         	| ...         	| ...         	| ...         	| ...         	|
| Liabilities & Shareholders' Equity  	| Total Shareholders' Equity / Assets 	| 8.47%       	| 8.73%       	| 8.41%       	| 8.80%       	| 8.48%       	|
|                                     	| Return On Average Total Equity      	| -           	| -           	| -           	| 10.26%      	| -           	|
|                                     	| Accumulated Minority Interest       	| 6.88B       	| 7.13B       	| 6.49B       	| 7.34B       	| 6.69B       	|
|                                     	| Total Equity                        	| 56B         	| 58.29B      	| 54.29B      	| 59.79B      	| 54.45B      	|
|                                     	| Liabilities & Shareholders' Equity  	| 579.79B     	| 586.09B     	| 568.11B     	| 596.33B     	| 562.95B     	|

[74 rows x 5 columns]


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get income statement
Get income statement data of a given symbol

**Args**:
- **`company`** `str`: Ticker symbol(e.g. 'IAM', 'MNG')
- **`frequency`** `str`: Display either quarter or annual data. Defaults to "annual".

**Returns**:
- **`pd.DataFrame`**: Dataframe of income statement data

**Example:**
```python
# Annual income statement
stm.get_income_statement('IAM', frequency='annual')
```

|**Item**                               | 2017   	| 2018   	| 2019    	| 2020    	| 2021   	|
|-------------------------------------	|--------	|--------	|---------	|---------	|--------	|
| Sales/Revenue                       	| 34.96B 	| 36.03B 	| 36.52B  	| 36.77B  	| 35.79B 	|
| Sales Growth                        	| -      	| 3.06%  	| 1.35%   	| 0.69%   	| -2.66% 	|
| Cost of Goods Sold (COGS) incl. D&A 	| 15.69B 	| 15.72B 	| 16.19B  	| 15.93B  	| 15.05B 	|
| COGS Growth                         	| -      	| 0.24%  	| 2.95%   	| -1.57%  	| -5.56% 	|
| COGS excluding D&A                  	| 9.08B  	| 8.9B   	| 8.77B   	| 8.42B   	| 7.99B  	|
| Non Operating Income/Expense        	| (57M)  	| 201M   	| (49M)   	| (1.49B) 	| (165M) 	|
| ...                                 	| ...    	| ...    	| ...     	| ...     	| ...    	|
| Equity in Affiliates (Pretax)       	| -      	| -      	| -       	| -       	| -      	|
| Interest Expense                    	| 586M   	| 642M   	| 756M    	| 888M    	| 826M   	|
| Interest Expense Growth             	| -      	| 9.56%  	| 17.76%  	| 17.46%  	| -6.98% 	|
| EBITDA                              	| 17.03B 	| 17.87B 	| 15.65B  	| 19.53B  	| 18.63B 	|
| EBITDA Growth                       	| -      	| 4.93%  	| -12.44% 	| 24.80%  	| -4.62% 	|
| EBITDA Margin                       	| -      	| -      	| -       	| -       	| 52.05% 	|

```python
# Quarter income statement
stm.get_income_statement('IAM', frequency='quarter')
```

|**Item**                               | 31-Dec-2019 	| 30-Jun-2020 	| 31-Dec-2020 	| 30-Jun-2021 	| 31-Dec-2021 	|
|-------------------------------------	|-------------	|-------------	|-------------	|-------------	|-------------	|
| Sales/Revenue                       	| 18.67B      	| 18.32B      	| 18.45B      	| 17.78B      	| 18.01B      	|
| Sales Growth                        	| -           	| -1.87%      	| 0.67%       	| -3.61%      	| 1.29%       	|
| Cost of Goods Sold (COGS) incl. D&A 	| 11.53B      	| 4.92B       	| 7.74B       	| 7.9B        	| 7.57B       	|
| COGS Growth                         	| -           	| -57.33%     	| 57.23%      	| 2.02%       	| -4.08%      	|
| COGS excluding D&A                  	| 4.42B       	| 4.16B       	| 4.26B       	| 4.09B       	| 3.91B       	|
| Depreciation & Amortization Expense 	| 7.12B       	| 759M        	| 3.48B       	| 3.81B       	| 3.67B       	|
| ...                                 	| ...         	| ...         	| ...         	| ...         	| ...         	|
| EBITDA                              	| 9.49B       	| 6.6B        	| 9.66B       	| 9.37B       	| 9.68B       	|
| EBITDA Growth                       	| -           	| -30.48%     	| 46.52%      	| -3.07%      	| 3.38%       	|
| EBITDA Margin                       	| -           	| -           	| -           	| -           	| 53.76%      	|


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get cash flow
Get cash flow data of a given symbol

**Args**:
- **`company`** `str`: Ticker symbol(e.g. 'IAM', 'MNG')
- **`frequency`** `str`: Display either quarter or annual data. Defaults to "annual".

**Returns**:
- **`pd.DataFrame`**: Dataframe of cash flow data

**Example:**
```python
# Annual cash flow
stm.get_cash_flow('IAM', frequency='annual')
```
|                      	|                                        	| 2017    	| 2018    	| 2019    	| 2020    	| 2021    	|
|----------------------	|----------------------------------------	|---------	|---------	|---------	|---------	|---------	|
|                      	| **Item**                                |         	|         	|         	|         	|         	|
| Operating Activities 	| Net Income before Extraordinaries      	| 10.31B  	| 11.05B  	| 8.23B   	| 12.02B  	| 11.57B  	|
|                      	| Net Income Growth                      	| -       	| 7.20%   	| -25.52% 	| 46.01%  	| -3.70%  	|
|                      	| Depreciation, Depletion & Amortization 	| 6.61B   	| 6.82B   	| 7.42B   	| 7.51B   	| 7.06B   	|
|                      	| ...                                    	| ...     	| ...     	| ...     	| ...     	| ...     	|
|                      	| Net Operating Cash Flow                	| 14.13B  	| 13.95B  	| 14.81B  	| 10.48B  	| 12.87B  	|
|                      	| Net Operating Cash Flow Growth         	| -       	| -1.32%  	| 6.22%   	| -29.28% 	| 22.80%  	|
|                      	| Net Operating Cash Flow / Sales        	| 40.42%  	| 38.71%  	| 40.57%  	| 28.49%  	| 35.95%  	|
| Investing Activities 	| Capital Expenditures                   	| (8.37B) 	| (8.08B) 	| (7.95B) 	| (4.14B) 	| (5.29B) 	|
|                      	| Capital Expenditures Growth            	| -       	| 3.52%   	| 1.56%   	| 47.91%  	| -27.75% 	|
|                      	| Capital Expenditures / Sales           	| -23.94% 	| -22.41% 	| -21.77% 	| -11.26% 	| -14.78% 	|
|                      	| ...                                    	| ...     	| ...     	| ...     	| ...     	| ...     	|
|                      	| Net Investing Cash Flow                	| (8.07B) 	| (8.37B) 	| (8.83B) 	| (4.23B) 	| (5.31B) 	|
|                      	| Net Investing Cash Flow Growth         	| -       	| -3.77%  	| -5.42%  	| 52.03%  	| -25.42% 	|
|                      	| Net Investing Cash Flow / Sales        	| -23.07% 	| -23.23% 	| -24.17% 	| -11.51% 	| -14.83% 	|
| Financing Activities 	| Cash Dividends Paid - Total            	| (5.6B)  	| (5.73B) 	| (6B)    	| (4.87B) 	| (3.53B) 	|
|                      	| Common Dividends                       	| (5.6B)  	| (5.73B) 	| (6B)    	| (4.87B) 	| (3.53B) 	|
|                      	| Preferred Dividends                    	| -       	| -       	| -       	| -       	| -       	|
|                      	| ...                                    	| ...     	| ...     	| ...     	| ...     	| ...     	|
|                      	| Free Cash Flow                         	| 5.76B   	| 5.87B   	| 6.87B   	| 6.34B   	| 7.58B   	|
|                      	| Free Cash Flow Growth                  	| -       	| 1.89%   	| 16.91%  	| -7.72%  	| 19.57%  	|
|                      	| Free Cash Flow Yield                   	| -       	| -       	| -       	| -       	| 3.30    	|

```python
# Quarter cash flow
stm.get_cash_flow('IAM', frequency='quarter')
```

|                      	|                                        	| 31-Dec-2019 	| 30-Jun-2020 	| 31-Dec-2020 	| 30-Jun-2021 	| 31-Dec-2021 	|
|----------------------	|----------------------------------------	|-------------	|-------------	|-------------	|-------------	|-------------	|
|                      	| **Item**                                |             	|             	|             	|             	|             	|
| Operating Activities 	| Net Income before Extraordinaries      	| 2.37B       	| 5.84B       	| 6.18B       	| 5.56B       	| 6.02B       	|
|                      	| Net Income Growth                      	| -           	| 146.35%     	| 5.93%       	| -10.11%     	| 8.26%       	|
|                      	| Depreciation, Depletion & Amortization 	| 3.81B       	| (759M)      	| 8.27B       	| 3.81B       	| 3.25B       	|
|                      	| ...                                    	| ...         	| ...         	| ...         	| ...         	| ...         	|
|                      	| Net Operating Cash Flow                	| 8.95B       	| 1.86B       	| 8.62B       	| 5.81B       	| 7.05B       	|
|                      	| Net Operating Cash Flow Growth         	| -           	| -79.27%     	| 364.44%     	| -32.56%     	| 21.31%      	|
|                      	| Net Operating Cash Flow / Sales        	| 47.94%      	| 10.13%      	| 46.73%      	| 32.69%      	| 39.16%      	|
| Investing Activities 	| Capital Expenditures                   	| (3.73B)     	| (2.29B)     	| (1.85B)     	| (2.74B)     	| (2.55B)     	|
|                      	| Capital Expenditures Growth            	| -           	| 38.69%      	| 18.93%      	| -47.57%     	| 6.65%       	|
|                      	| Capital Expenditures / Sales           	| -19.98%     	| -12.48%     	| -10.05%     	| -15.39%     	| -14.18%     	|
|                      	| ...                                    	| ...         	| ...         	| ...         	| ...         	| ...         	|
|                      	| Net Investing Cash Flow                	| (3.56B)     	| (2.4B)      	| (1.84B)     	| (2.76B)     	| (2.55B)     	|
|                      	| Net Investing Cash Flow Growth         	| -           	| 32.71%      	| 23.40%      	| -50.11%     	| 7.37%       	|
|                      	| Net Investing Cash Flow / Sales        	| -19.08%     	| -13.08%     	| -9.95%      	| -15.50%     	| -14.18%     	|
| Financing Activities 	| Cash Dividends Paid - Total            	| (271M)      	| -           	| (4.87B)     	| -           	| (3.53B)     	|
|                      	| Common Dividends                       	| (271M)      	| -           	| (4.87B)     	| -           	| (3.53B)     	|
|                      	| Preferred Dividends                    	| -           	| -           	| -           	| -           	| -           	|
|                      	| ...                                    	| ...         	| ...         	| ...         	| ...         	| ...         	|
|                      	| Free Cash Flow                         	| 5.22B       	| (431M)      	| 6.77B       	| 3.08B       	| 4.5B        	|
|                      	| Free Cash Flow Growth                  	| -           	| -108.25%    	| 1,669.84%   	| -54.52%     	| 46.18%      	|
|                      	| Free Cash Flow Yield                   	| -           	| -           	| -           	| -           	| 3.30        	|


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get quote table
Get important data about a given symbol

**Args**:
- **`company`** `str`: Ticker symbol(e.g. 'IAM', 'MNG')

**Returns**:
- **`pd.DataFrame`**: Dataframe of data about the ticker

**Example:**
```python
stm.get_quote_table('ATW')
```

|    	| Key Data           	| Value           	|
|----	|--------------------	|-----------------	|
| 0  	| Open               	| 473.00          	|
| 1  	| Day Range          	| 464.00 - 473.00 	|
| 2  	| 52 Week Range      	| N/A             	|
| 3  	| Market Cap         	| 93.69B          	|
| 4  	| Shares Outstanding 	| 215.14M         	|
| 5  	| Public Float       	| 69.09M          	|
| 6  	| Beta               	| N/A             	|
| 7  	| Rev. per Employee  	| 1.933M          	|
| 8  	| P/E Ratio          	| 18.04           	|
| 9  	| EPS                	| 25.72           	|
| 10 	| Yield              	| 3.23%           	|
| 11 	| Dividend           	| 6.75            	|
| 12 	| Ex-Dividend Date   	| Jul 5, 2021     	|
| 13 	| Short Interest     	| N/A             	|
| 14 	| % of Float Shorted 	| N/A             	|
| 15 	| Average Volume     	| 160.21K         	|


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get market status
Get status of the Moroccan market
**Returns**:
- **`str`**: Status of the market(Open/Closed)

**Example:**
```python
stm.get_market_status()
```
```bash
Closed
```


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get company officers
Get company officers of a given symbol

**Args**:
- **`company`** `str`: Ticker symbol(e.g. 'IAM', 'MNG')

**Returns**:
- **`pd.DataFrame`**: Dataframe of names and roles of the officers

**Example:**
```python
stm.get_company_officers('MNG')
```

|    	| Name                   	| Role                                              	|
|----	|------------------------	|---------------------------------------------------	|
| 0  	| Imad Toumi             	| Chairman & Chief Executive Officer                	|
| 1  	| Mouna Mahfoud          	| Executive Director-Finance                        	|
| 2  	| Naoual Zine            	| General Manager-Reminex & Projects                	|
| 3  	| Lhou Maacha            	| Executive Director-Exploration                    	|
| 4  	| Youssef el Hajjam      	| General Manager-Bases Metal Operations            	|
| 5  	| Karim Khettouch        	| Director                                          	|
| 6  	| Samir Oudghiri Idrissi 	| Director                                          	|
| 7  	| Bassim Jaï Hokimi      	| Director                                          	|
| 8  	| Hassan Ouriagli        	| Director                                          	|
| 9  	| Amina Benkhadra        	| Director                                          	|
| 10 	| Noufissa Kessar        	| Director                                          	|
| 11 	| Mohamed Amine Afsahi   	| Executive Director-Marketing & Commercial         	|
| 12 	| Laila Karam            	| Investor Relations Contact                        	|
| 13 	| Zakaria Rbii           	| Executive Director-HR, Communication & Develop... 	|
| 14 	| Frédéric Bernard Tona  	| Independent Director                              	|


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

### Get company information
Get information related to the company's location, adresse...

**Args**:
- **`company`** `str`: Ticker symbol(e.g. 'IAM', 'MNG')

**Returns**:
- **`pd.DataFrame`**: Dataframe of information related to the company (e.g. Name, Adresse, Phone...)

**Example:**
```python
stm.get_company_info('MNG')
```

|   	| Item        	| Value                                             	|
|---	|-------------	|---------------------------------------------------	|
| 0 	| Name        	| Managem                                           	|
| 1 	| Adresse     	| Twin Center, Tower A Angle Boulevards Zerktoun... 	|
| 2 	| Phone       	| +212 522 956-565                                  	|
| 3 	| Industry    	| General Mining                                    	|
| 4 	| Sector      	| Basic Materials/Resources                         	|
| 5 	| Description 	| Managem SA engages in mining and hydrometallur... 	|


<div align="right"><a href="#usage" style="float: right;font-size: 12px;font-weight: bold;">Back to top</a></div>


---

## License
This project is licensed under the terms of the MIT license.
