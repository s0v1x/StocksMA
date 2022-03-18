<div align="center">
  <hr />
  <p>
      <img width="500" src="stocks.png" alt="StocksMA" />
      

  </p>
  <b>Creating easier access to the Moroccan stock market data</b>
  
  <br />
</div>

---
<div align="center">

[![Language](https://img.shields.io/badge/Language-Python-green?style)](https://github.com/s0v1x)
[![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flatcolor=BC4E99)](https://github.com/s0v1x/EULERA)
[![GitHub license](https://img.shields.io/github/license/s0v1x/EULERA)](https://github.com/s0v1x/EULERA/blob/master/LICENSE)
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


## Import the package

```python
$ import StocksMA as stm
```

#### Get all availabale tickers


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

#### Get price data

```python
# Get price data of multiple companies
stm.get_price_data(['CIH','maroc telecom', 'mng'], start_date='2020-11-14', end_date='2022-02-14')
```
|           	|            	| Close  	| High   	| Low    	| Open   	| Volume 	|
|-----------	|------------	|--------	|--------	|--------	|--------	|--------	|
| **Company**   | **Date**      |        	|        	|        	|        	|        	|
| CIH P     	| 2020-11-16 	| 248.15 	| 248.15 	| 248.00 	| 248.00 	| 8      	|
|           	| 2020-11-17 	| 250.00 	| 250.00 	| 248.00 	| 248.10 	| 220    	|
|           	| 2020-11-19 	| 245.20 	| 248.00 	| 245.10 	| 248.00 	| 133    	|
|           	| ...        	| ...    	| ...    	| ...    	| ...    	| ...    	|
| INVOLYS P 	| 2022-02-08 	| 131.95 	| 131.95 	| 131.95 	| 131.95 	| 5      	|
|           	| 2022-02-09 	| 131.95 	| 131.95 	| 131.90 	| 131.95 	| 100    	|
|           	| 2022-02-11 	| 131.90 	| 131.90 	| 131.00 	| 131.00 	| 4      	|
<p>[840 rows x 5 columns]</p>


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
<p>[253 rows x 5 columns]</p>

#### Get quick information about the company

```python
stm.get_quick_info('involys')
```

|   	| Name      	| Name_2  	| ISIN         	| Number of Shares 	| Close   	| Previous Close 	| Market Cap  	| Quotation Datetime 	|  Change Volume 	| Change 	| Volume in Shares 	| Volume 	| Open    	| Low     	| High    	|
|---	|-----------	|---------	|--------------	|------------------	|---------	|----------------	|-------------	|--------------------	|----------------	|--------	|------------------	|--------	|---------	|---------	|---------	|
| 1 	| INVOLYS P 	| INVOLYS 	| MA0000011579 	| 382716           	| 109.950 	| 109.95         	| 42079624.20 	| 18/03/2022 à 15:16 	| 0.00           	| 0.00   	| 5387             	| 49     	| 109.400 	| 109.400 	| 109.950 	|

#### Get intraday price data

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

#### Get Ask Bid data

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

#### Get balance sheet

```python
# Annual balance sheet
stm.get_balance_sheet('ATW', period='annualy')
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
stm.get_balance_sheet('ATW', period='quarter')
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

#### Get income statement

```python
# Annual income statement
stm.get_income_statement('IAM', period='annual')
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
stm.get_income_statement('IAM', period='quarter')
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

#### Get cash flow

```python
# Annual cash flow
stm.get_cash_flow('IAM', period='annual')
```