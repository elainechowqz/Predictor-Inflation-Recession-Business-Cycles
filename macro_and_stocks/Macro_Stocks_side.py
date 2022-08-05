# Goal: study the relations between macroecomic indicators and stock market prices, especially given that these days the behavior of inflation relative to the entire economy seems to have changed; then specifically study if macroeconomic conditions are predictive of the returns of the total stock market or certain groups of stocks like growth, value, tech, emerging markets, etc. 

# Original project description: 
# Relationship between macroeconomic indicators and the stock market. The first objective of this project will be to download historical data on various macroeconomic indicators (such as inflation, GDP, industrial production, corporate bond yields, treasury yields, money supply, oil price) using the ALFRED and FRED databases from the Federal Reserve Bank in St. Louis, as well as WRDS. The second objective will be to use clustering methods to group together time periods with similar macroeconomic conditions. The third objective will be to investigate whether similar stock market behaviors are observed during different time periods with similar macroeconomic conditions. For example, are macroeconomic conditions predictive of the total stock market returns (as measured by, for example, S&P 500)? Do growth stocks tend to outperform value stocks after (or during) certain macroeconomic conditions and underperform them after (or during) certain other macroeconomic conditions? Here, "growth" refers to high price-to-book ratios and "value" refers to low price-to-book ratios. Same question regarding small vs large stocks (e.g. the smallest companies in S&P 500 by market capitalization vs the largest companies).
# https://engineering.purdue.edu/~ipollak/ece695/SPRING10/project_topics.html 

# one current context: The “Economist” magazine Oct 12th – Oct 18th 2019 issue. Special report on inflation in today’s world plus Leaders section: “The world economy’s strange new rules”.
# think about how this new economic phenomenon would affect the stock markets and other financial products and businesses. 

# need to ask questions out of business interests, not just curiosities; outcomes should be measurable and relatively specific, and not just about the entire society, etc. 

import pandas as pd
import pandas_datareader as pdr
import datetime 
import numpy as np
import matplotlib.pyplot as plt
# Import the `api` model of `statsmodels` under alias `sm`
import statsmodels.api as sm

# 1. Compare the statistical relations between seasonally adjusted unemployment rates and S&P 500 over the 5-year periods Sep 2009 – Sep 2014 and Oct 2014 – Oct 2019, and then extend the analysis to all the available historical data (which span over about 6 decades). For instance, what do various statistical criteria like correlation mean? Perhaps I need to change the S&P 500 stock prices to monthly rates of changes, etc. 
# These two 5-year periods were chosen by me after looking at the graph for unemployment rates. This choice is a bit ad hoc and needs to be replaced with machine learning (clustering) later on. 



# 1.0: Obtain historical data for various macroeconomic indicators(presented monthly); upload the data for inflation and unemployment for the time periods given above; obtain S&P 500 prices (represented by oldest ETF "SPY") for the time periods given above(presented daily) and build a new dataframe whose columns are the prices at the first day of each month, as well as monthly changes.  

#a function that converts an Excel file to a Pandas dataframe:
def get_data(file_path):
    return pd.read_excel (file_path)

# obtain monthly unemployment and inflation data for Sep 2009 – Sep 2014 and Oct 2014 – Oct 2019
unemp1 = get_data('/Users/elainemulan/Macroeconomic Indicators some historical data/Step 1/US seasonally adjusted unemployment rate Sep 2009 - Sep 2014.xlsx')
unemp2 = get_data('/Users/elainemulan/Macroeconomic Indicators some historical data/Step 1/US seasonally adjusted unemployment rate Oct 2014 - Oct 2019.xlsx')
inflat1 = get_data('/Users/elainemulan/Macroeconomic Indicators some historical data/Step 1/US seasonally adjusted urban CPI Sep 2009 - Sep 2014.xlsx')
inflat2 = get_data('/Users/elainemulan/Macroeconomic Indicators some historical data/Step 1/US seasonally adjusted urban CPI Oct 2014 - Oct 2019.xlsx')

# obtain the daily data of S&P 500 ETF "SPY" data for Sep 2009 - Sep 2014 and Oct 2014 - Oct 2019 as a dataframe, and convert that to a monthly dataframe of stock prices as well as monthly percentage changes

# getting daily stock prices data
sp500_1 = pdr.get_data_yahoo('SPY', datetime.datetime(2009, 9, 1), datetime.datetime(2014, 9, 1))
sp500_2 = pdr.get_data_yahoo('SPY', datetime.datetime(2014, 10, 1), datetime.datetime(2019, 10, 1))

# picking the adjusted closing prices for the first day of each month
#sp500mon_1 = sp500_1['Adj Close'].loc[sp500_1.index.day == 1]
#sp500mon_2 = sp500_2['Adj Close'].loc[sp500_2.index.day == 1]
#sp500mon_1 = sp500mon_1.to_frame()
#sp500mon_2 = sp500mon_2.to_frame()
#problems: there is no stock market data if the first day of the month is a weekend day; change it to the next row of the ETF dataframe if those months are not skipped for the macroeconomic indicators. 
#strategy 1: set sp500mon_1 and sp500mon_2 to have the same index as that of the macroeconomic indicators, and no need to get all the daily S&P 500 data during the time range. For a given date (first day of a month) in the index, just use "pdr.get_data_yahoo('SPY', datetime.datetime(), datetime.datetime())" for the same start and end date, and we get the stock price for the next weekday of the given date. 
#problems of strategy1: pdr.get_data_yahoo returns a dataframe(not a number) involving two days for weekdays, one day for Sundays, and error messages for Saturdays. Solution: for weekdays and Sundays, take the adjusted closed price for the first row; for Saturdays, consider the next day. However, this doesn't work for some holidays, like Jan 1st - Jan 2nd 2010 return error messages. 
# Solution: We need to make use of the daily stock data. Take the first day with available stocks data for each month? e.g. while the given date is not in the index of sp500_1 or sp500_2, add one day. 
#Or another better choice statistically? https://www.researchgate.net/post/how_to_derive_a_monthly_representative_value_for_the_daily_series_of_stock_prices

sp500mon_1 = unemp1[['observation_date']]
sp500mon_2 = unemp2[['observation_date']]

stocks1 = []
daystocks1 = []
for d in sp500_1.index:
    date = d.to_pydatetime()
    daystocks1.append(date)
    
for i in sp500mon_1.index:
    timestamp = sp500mon_1.loc[i, 'observation_date']
    #date = datetime.datetime.fromtimestamp(timestamp)
    date = timestamp.to_pydatetime()
    while date not in daystocks1:
        date += datetime.timedelta(days=1)
    closing_price = pdr.get_data_yahoo('SPY', date, date).iloc[0,5]
    stocks1.append(closing_price)
sp500mon_1['S&P 500 prices'] = stocks1

stocks2 = []
daystocks2 = []
for d in sp500_2.index:
    date = d.to_pydatetime()
    daystocks2.append(date)
    
for i in sp500mon_2.index:
    timestamp = sp500mon_2.loc[i, 'observation_date']
    #date = datetime.datetime.fromtimestamp(timestamp)
    date = timestamp.to_pydatetime()
    while date not in daystocks2:
        date += datetime.timedelta(days=1)
    closing_price = pdr.get_data_yahoo('SPY', date, date).iloc[0,5]
    stocks2.append(closing_price)
sp500mon_2['S&P 500 prices'] = stocks2

# compute the monthly percentage changes (or some other related quantities like log) for inflation, unemployment rates and stock merket prices during the given time periods. 

# function that computes monthly changes and their logs for the items in a given column of macroeconomic or stocks data
def percent_change(df):
    return (df - df.shift(1))/df.shift(1)

#advantages of using log:https://www.forbes.com/sites/naomirobbins/2012/01/19/when-should-i-use-logarithmic-scales-in-my-charts-and-graphs/#55d59f45e67b. See financeanalysis1.py and Python for Finance course at DataCamp.
def log_ratio(df):
    return np.log(df/df.shift(1))
    
#find the percentage and log changes for unemployment rates, inflation and S&P 500 prices for the given two time periods. 

def add_stats_columns(df):
    col = df.iloc[:, -1].to_frame()
    per_change = percent_change(col)
    df['monthly percent change'] = per_change
    log = log_ratio(col)
    df['monthly log ratio'] = log
    
indicatorsandstockslist = [unemp1, unemp2, inflat1, inflat2, sp500mon_1, sp500mon_2]

for x in indicatorsandstockslist:
    add_stats_columns(x)




# 1.1: Compute the correlations and other statistical factors(e.g. hypothesis testing? statistical inference?) between inflation, unemployment rate and S&P 500 prices. What do they mean? e.g. hypothesis: the correlations between unemployment and inflation are constant. test it. 

# 2. To explain the differences in statistical relations observed in Step 1, we add in all the other macroeconomic conditions (e.g. housing prices, GDP, etc) and use unsupervised learning to decide on the time periods. More specifically, we use clustering to group together time periods with similar macroeconomic conditions. 
# Do note that there is no need to adjust macroeconomic conditions like prices or GDP for inflation, as inflation itself is an important macroeconomic indicator, and the stock market prices are affected by inflation as well. 

# 3. Investigate whether similar stock market behaviors are observed during different time periods with similar macroeconomic conditions. For example, are macroeconomic conditions predictive of the total stock market returns (as measured by, for example, S&P 500)? Do growth stocks tend to outperform value stocks after (or during) certain macroeconomic conditions and underperform them after (or during) certain other macroeconomic conditions? Here, "growth" refers to high price-to-book ratios and "value" refers to low price-to-book ratios. Same question regarding small vs large stocks (e.g. the smallest companies in S&P 500 by market capitalization vs the largest companies).
# In particular, in today's new economic conditions of low inflation, how do macroeconomic conditions (the usual plus globalization, tech, etc) affect stock prices? 