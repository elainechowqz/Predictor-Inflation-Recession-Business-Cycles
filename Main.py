import pandas as pd
import pandas_datareader as pdr
import datetime 
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import scipy.stats
import statsmodels.api as sm
import macroeconomics as mac
import macroeconomics2 as mac2
from sklearn.linear_model import LinearRegression


# Part Zero: prepare a dataframe for S&P 500 data over half of a century

# Get S&P 500 index data from Yahoo Finance

start_date = datetime.date(1970, 1, 1)
end_date = datetime.date(2021, 2, 23)

price = pdr.get_data_yahoo('^GSPC', start_date, end_date)

# Compute daily, weekly, monthly and yearly percentage returns, as well as monthly log returns
price['daily_return'] = (price['Adj Close']/ price['Adj Close'].shift(1)) -1
# Shift = 7 - 2(weekend) = 5
price['weekly_return'] = (price['Adj Close']/ price['Adj Close'].shift(5)) -1

# Since there is no stock market data on weekends, we shift 30-4 weekends = 22 days to estimate monthly return
price['monthly_return'] = (price['Adj Close']/ price['Adj Close'].shift(21)) -1
price['monthly_log_return'] = price['monthly_log_return'] = np.log(price['Adj Close']/ price['Adj Close'].shift(22))

# For annual returns, shift = 365 - 52*2(weekends) - 10 annual federal holidays = 251
price['yearly_return'] = (price['Adj Close']/ price['Adj Close'].shift(251)) -1

# Set up new columns for returns over different time periods
daily = price['daily_return']
weekly = price['weekly_return']
monthly = price['monthly_return']
yearly = price['yearly_return']
monthly_log = price['monthly_log_return']

daily.dropna(inplace = True)
weekly.dropna(inplace = True)
monthly.dropna(inplace = True)
yearly.dropna(inplace = True)
monthly_log.dropna(inplace = True)


# Part One: point estimation for the mean, standard deviation, and the coefficient of variation(a statistical measure of relative variability) for the returns

def point_stats_estimation(dfcolumn, name):
    print(name, dfcolumn.mean(), dfcolumn.std(), dfcolumn.std()/dfcolumn.mean())
    
point_stats_estimation(daily, 'daily_return')
point_stats_estimation(weekly, 'weekly_return')
point_stats_estimation(monthly, 'monthly_return')
point_stats_estimation(yearly, 'yearly_return')
point_stats_estimation(monthly_log, 'monthly_log_return')


# Part Two: understand more about the probability distribution of the returns

# Approach 1: since mean and variance of returns don't stay constant over time, we choose to focus on a short time period and test the normality assumption
# Use short term data(data from 1970s) and some standard statistical tests for normality on daily, weekly and monthly returns+log returns

def statistical_tests_for_short_term(pricedf, start_date, end_date, colname):
    price_shortterm = pricedf[start_date : end_date]
    col_shortterm = price_shortterm[colname]
    col_shortterm.dropna(inplace = True)
    a = col_shortterm.to_numpy()
    print(colname, 'D’Agostino and Pearson’s test', scipy.stats.normaltest(a, axis=0, nan_policy='propagate'))
    print(colname, ' the Shapiro-Wilk test for normality', scipy.stats.shapiro(a))
    print(colname, 'Anderson-Darling test for data coming from a particular distribution', scipy.stats.anderson(a))
    print(colname, 'Kolmogorov-Smirnov test for goodness of fit', scipy.stats.kstest(a, 'norm', N=len(a), alternative='two-sided'))

d1 = '19700102'
d2 = '19751230'
statistical_tests_for_short_term(price, d1, d2, 'daily_return')
statistical_tests_for_short_term(price, d1, d2, 'weekly_return')
statistical_tests_for_short_term(price, d1, d2, 'monthly_return')
statistical_tests_for_short_term(price, d1, d2, 'monthly_log_return')

# Upshot: using the four statistical tests above, we see that all the p-values(as compared to the standard cutoff 0.5) and critical values are ridiculously off. Normality Hypothesis rejected for returns during year 1970 as well as the five year period 1970-1975. 

# Approach 2: after reading some online articles, I realized that stocks returns are more or less normal except for a much fatter tail. Therefore, while the normality assumption is rejected under various statistical tests, it is still useful. However, the fat tail needs to be taken into account of. 
# We now use 50 years of data on monthly returns, and perform some graphical inspections for the normality assumption. 

# QQ plots for daily and monthly returns over 5 decades

# Normalize daily and monthly data so as to compare with standard normal distribution

monthly_mean = monthly.mean()
monthly_std = monthly.std()
daily_mean = daily.mean()
daily_std = daily.std()
monthlylog_mean = monthly_log.mean()
monthlylog_std = monthly_log.std()
price['normalized monthly'] = (price['monthly_return'] - monthly_mean)/monthly_std
price['normalized daily'] = (price['daily_return'] - daily_mean)/daily_std
price['normalized monthlylog'] = (price['monthly_log_return'] - monthlylog_mean)/monthlylog_std

monthly_normalized = price['normalized monthly']
monthly_normalized.dropna(inplace = True)
daily_normalized = price['normalized daily']
daily_normalized.dropna(inplace = True)
monthlylog_normalized = price['normalized monthlylog']
monthlylog_normalized.dropna(inplace = True)

sm.qqplot(monthly_normalized.to_numpy(), line='45')
plt.show()

sm.qqplot(monthlylog_normalized.to_numpy(), line='45')
plt.show()

sm.qqplot(daily_normalized.to_numpy(), line='45')
plt.show()

# From the QQ plots, we see that both ends of the plot deviate significantly from the straight line, and its center fits the line pretty well. This suggest that our probability distribution has fat tails. 


#Part 3: Statistical analysis of two macroeconomic indicators: CPI & Unemployment Rate vs S&P 500 

# We could either work with normalized or standardized data

normalized_macro = mac.Inflation_Unemploymt_df2
standardized_macro = mac2.Inflation_Unemploymt_df2
normalized_num = mac.num
standardized_num = mac2.num

num = standardized_num
chosen_macrodata = standardized_macro
chosen_macrodata.reset_index()
color_list = mac.color_list

# Resample daily data and get monthly data 
monthly_price = price[['Adj Close', 'monthly_return']].resample('MS').first()
monthly_price_avg = price[['Adj Close', 'monthly_return']].resample('MS').mean()

# Merge macroeconomic and stocks data into the same dataframe 
mp = monthly_price.reset_index().rename(columns={"Date": "observation_date", "Adj Close": "Adj Close", "monthly_return": "monthly_return"})
mpa = monthly_price_avg.reset_index().rename(columns={"Date": "observation_date", "Adj Close": "Avg Adj Close", "monthly_return": "avg_monthly_return"})

macro_stocks_df1 = pd.merge(chosen_macrodata, mp, on='observation_date')
macro_stocks_df2 = pd.merge(macro_stocks_df1, mpa)
macro_stocks_df = macro_stocks_df2.dropna(axis=0)

# Make a list of clusters

cluster_list = []

for i in range(num):
    cluster_df = macro_stocks_df.loc[macro_stocks_df['cluster'] == i]
    cluster_list.append(cluster_df)

# Approach One: linear regression for each cluster --- the dependent variables are unemployment and inflation rates, and the independent variable is the rate of return for stocks 

coef_list = []
dependent_v = 'monthly_return'

for j in range(len(cluster_list)):
    lr = LinearRegression()
    #select the columns for unemployment rate and annual inflation rate
    X_train = cluster_list[j].iloc[:, [3, 6]]
    Y_train = cluster_list[j][dependent_v]
    lr.fit(X_train,Y_train) 
    intercept = lr.intercept_
    coef = lr.coef_
    coef_list.append([intercept, coef])
    
# Compute the R-squared values for the regressions corresponding to individual clusters

quotient_list = []
for j in range(len(coef_list)):
    w_0 = coef_list[j][0]
    w_1 = coef_list[j][1][0]
    w_2 = coef_list[j][1][1]
    cluster_df = cluster_list[j]
    mean = cluster_df[dependent_v].sum()/cluster_df.shape[0]
    total_var = ((cluster_df[dependent_v] - mean)**2).sum()
    cluster_df['prediction'] = w_0 + w_1*cluster_df.iloc[:, 3] + w_2*cluster_df.iloc[:, 6]
    error_var = ((cluster_df[dependent_v] - cluster_df['prediction'] )**2).sum()
    regression_var = ((cluster_df['prediction'] - mean)**2).sum()
    quot = regression_var/total_var
    quotient_list.append(quot)
    
# UPshot: It turns out that the R-squared values all clusters and all forms of macroeconomic data(normalized, standardized or raw) are all really small, much less than 0.05. So linear regression is a bad idea. 
    
# More data visualization: general scatter plots in 2d and 3d

macsto = macro_stocks_df.iloc[:, [4, 6, 10]].to_numpy()

plt.figure()
for i in range(num):
    plt.scatter(macsto[macro_stocks_df['cluster'] == i, 0], macsto[macro_stocks_df['cluster'] == i, 1], s = 50, c = color_list[i])

plt.figure()
for i in range(num):
    plt.scatter(macsto[macro_stocks_df['cluster'] == i, 0], macsto[macro_stocks_df['cluster'] == i, 2], s = 50, c = color_list[i])
    
plt.figure()
for i in range(num):
    plt.scatter(macsto[macro_stocks_df['cluster'] == i, 1], macsto[macro_stocks_df['cluster'] == i, 2], s = 50, c = color_list[i])
    
fig = plt.figure()
ax = plt.axes(projection='3d')
for i in range(num):
    ax.scatter3D(macsto[macro_stocks_df['cluster'] == i, 0], macsto[macro_stocks_df['cluster'] == i, 1], macsto[macro_stocks_df['cluster'] == i, 2], c = color_list[i])
    
# More data visualization: histogram plots for monthly returns within each cluster

for i in range(num):
    mchange = cluster_list[i]['monthly_return'].to_list()
    plt.figure()
    plt.hist(mchange, bins=10, label = i)
    plt.legend()
    print(i, cluster_list[i]['monthly_return'].describe())
    
    
# Approach Two: Instead of performing any regression analysis between the macroeconomic and stock market variables, we use the clustering results to classify the time periods according to different macroeconomic climates. In each cluster, we then study the stock market data directly and obtain various statistical measures like mean, variance and so on. 

# To be continued......




    


    



















