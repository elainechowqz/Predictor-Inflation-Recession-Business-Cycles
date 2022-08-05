import pandas as pd
import pandas_datareader as pdr
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import scipy.stats
import statsmodels.api as sm
import macroeconomics_normalized_data as mac
import macroeconomics_standardized_data as mac2
from sklearn.linear_model import LinearRegression
from pandas.tseries.offsets import DateOffset

# getting S&P 500 index from Yahoo Finance

start_date = datetime.date(1970, 1, 1)
end_date = datetime.date(2022, 8, 3)

price = pdr.get_data_yahoo('^GSPC', start_date, end_date)

# compute daily, weekly, monthly and yearly percentage returns, as well as monthly log returns
price['daily_return'] = (price['Adj Close'] / price['Adj Close'].shift(1)) - 1
# shift = 7 - 2(weekend) = 5
price['weekly_return'] = (price['Adj Close'] / price['Adj Close'].shift(5)) - 1
# Since there is no stock market data on weekends, we shift 21 days to calculate monthly return
price['monthly_return'] = (
    price['Adj Close'] / price['Adj Close'].shift(21)) - 1
# shift = 365 - 52*2(weekends) - 10 annual federal holidays = 251
price['yearly_return'] = (
    price['Adj Close'] / price['Adj Close'].shift(251)) - 1
price['monthly_log_return'] = price['monthly_log_return'] = np.log(
    price['Adj Close'] / price['Adj Close'].shift(22))


daily = price['daily_return']
weekly = price['weekly_return']
monthly = price['monthly_return']
yearly = price['yearly_return']
monthly_log = price['monthly_log_return']

daily.dropna(inplace=True)
weekly.dropna(inplace=True)
monthly.dropna(inplace=True)
yearly.dropna(inplace=True)
monthly_log.dropna(inplace=True)


# Part 1: point estimation
def point_stats_estimation(dfcolumn, name):
    print(name, dfcolumn.mean(), dfcolumn.std(),
          dfcolumn.std()/dfcolumn.mean())


point_stats_estimation(daily, 'daily_return')
point_stats_estimation(weekly, 'weekly_return')
point_stats_estimation(monthly, 'monthly_return')
point_stats_estimation(yearly, 'yearly_return')
point_stats_estimation(monthly_log, 'monthly_log_return')


# Part 2: normality testing for data over a short period(one year) and interval estimation(based on normality assumption on the statistical distribution of returns)

# approach 1: use short term data(data from 1970) and some standard statistical tests for normality on daily, weekly and monthly returns+log returns

def statistical_tests_for_short_term(pricedf, start_date, end_date, colname):
    price_shortterm = pricedf[start_date: end_date]
    col_shortterm = price_shortterm[colname]
    col_shortterm.dropna(inplace=True)
    a = col_shortterm.to_numpy()
    print(colname, 'D’Agostino and Pearson’s test',
          scipy.stats.normaltest(a, axis=0, nan_policy='propagate'))
    print(colname, ' the Shapiro-Wilk test for normality', scipy.stats.shapiro(a))
    print(colname, 'Anderson-Darling test for data coming from a particular distribution',
          scipy.stats.anderson(a))
    print(colname, 'Kolmogorov-Smirnov test for goodness of fit',
          scipy.stats.kstest(a, 'norm', N=len(a), alternative='two-sided'))


d1 = '19700102'
d2 = '19751230'
statistical_tests_for_short_term(price, d1, d2, 'daily_return')
statistical_tests_for_short_term(price, d1, d2, 'weekly_return')
statistical_tests_for_short_term(price, d1, d2, 'monthly_return')
statistical_tests_for_short_term(price, d1, d2, 'monthly_log_return')

# upshot: using the four statistical tests above, we see that all the p-values(as compared to the standard cutoff 0.5) and critical values are ridiculously off. Normality Hypothesis rejected for returns during year 1970 as well as the five year period 1970-1975.


# approach 2: after reading an online article, I realized that stocks returns are more or less normal except for a much fatter tail. Therefore, the normality assumption is rejected under various statistical tests, it is still useful, but the fat tail needs to be taken into account of.
# I would like to now use 50 years of data on monthly returns, and perform some graphical normality inspections.

# QQ plots for daily and monthly returns over 5 decades

# normalize daily and monthly so as to compare with standard normal
monthly_mean = monthly.mean()
monthly_std = monthly.std()
daily_mean = daily.mean()
daily_std = daily.std()
monthlylog_mean = monthly_log.mean()
monthlylog_std = monthly_log.std()
price['normalized monthly'] = (
    price['monthly_return'] - monthly_mean)/monthly_std
price['normalized daily'] = (price['daily_return'] - daily_mean)/daily_std
price['normalized monthlylog'] = (
    price['monthly_log_return'] - monthlylog_mean)/monthlylog_std


monthly_normalized = price['normalized monthly']
monthly_normalized.dropna(inplace=True)
daily_normalized = price['normalized daily']
daily_normalized.dropna(inplace=True)
monthlylog_normalized = price['normalized monthlylog']
monthlylog_normalized.dropna(inplace=True)

sm.qqplot(monthly_normalized.to_numpy(), line='45')
plt.show()

sm.qqplot(monthlylog_normalized.to_numpy(), line='45')
plt.show()

sm.qqplot(daily_normalized.to_numpy(), line='45')
plt.show()


# Part 3: Statistical analysis of two macroeconomic indicators: CPI & Unemployment Rate vs S&P 500

normalized_macro = mac.Inflation_Unemploymt_df2
standardized_macro = mac2.Inflation_Unemploymt_df2
normalized_num = mac.num
standardized_num = mac2.num

num = standardized_num
chosen_macrodata = standardized_macro
chosen_macrodata.reset_index()
color_list = mac.color_list

# resample daily data and get monthly data
monthly_price = price[['Adj Close', 'monthly_return']].resample('MS').first()
monthly_price_avg = price[['Adj Close',
                           'monthly_return']].resample('MS').mean()

# merge macroeconomic and stocks data into the same dataframe
mp = monthly_price.reset_index().rename(columns={
    "Date": "observation_date", "Adj Close": "Adj Close", "monthly_return": "monthly_return"})
mpa = monthly_price_avg.reset_index().rename(columns={
    "Date": "observation_date", "Adj Close": "Avg Adj Close", "monthly_return": "avg_monthly_return"})

macro_stocks_df1 = pd.merge(chosen_macrodata, mp, on='observation_date')
macro_stocks_df2 = pd.merge(macro_stocks_df1, mpa)
macro_stocks_df = macro_stocks_df2.dropna(axis=0)

# make a list according to clustering
cluster_list = []


for i in range(num):
    cluster_df = macro_stocks_df.loc[macro_stocks_df['cluster'] == i]
    cluster_list.append(cluster_df)

# linear regression for each cluster

coef_list = []
dependent_v = 'monthly_return'

for j in range(len(cluster_list)):
    lr = LinearRegression()
    # select the columns for unemployment rate and annual inflation rate
    X_train = cluster_list[j].iloc[:, [3, 6]]
    Y_train = cluster_list[j][dependent_v]
    lr.fit(X_train, Y_train)
    intercept = lr.intercept_
    coef = lr.coef_
    coef_list.append([intercept, coef])

# analysis of variances for the linear regressions
quotient_list = []
for j in range(len(coef_list)):
    w_0 = coef_list[j][0]
    w_1 = coef_list[j][1][0]
    w_2 = coef_list[j][1][1]
    cluster_df = cluster_list[j]
    mean = cluster_df[dependent_v].sum()/cluster_df.shape[0]
    total_var = ((cluster_df[dependent_v] - mean)**2).sum()
    cluster_df['prediction'] = w_0 + w_1 * \
        cluster_df.iloc[:, 3] + w_2*cluster_df.iloc[:, 6]
    error_var = ((cluster_df[dependent_v] - cluster_df['prediction'])**2).sum()
    regression_var = ((cluster_df['prediction'] - mean)**2).sum()
    quot = regression_var/total_var
    quotient_list.append(quot)

# It turns out that the R2 score for any cluster, any form of macroeconomic data(normalized, standardized or raw) is all really small, less than 0.05. So linear regression is a bad idea.


# general scatter plots in 2d and 3d

macsto = macro_stocks_df.iloc[:, [4, 6, 10]].to_numpy()

plt.figure()
for i in range(num):
    plt.scatter(macsto[macro_stocks_df['cluster'] == i, 0],
                macsto[macro_stocks_df['cluster'] == i, 1], s=50, c=color_list[i])

plt.figure()
for i in range(num):
    plt.scatter(macsto[macro_stocks_df['cluster'] == i, 0],
                macsto[macro_stocks_df['cluster'] == i, 2], s=50, c=color_list[i])

plt.figure()
for i in range(num):
    plt.scatter(macsto[macro_stocks_df['cluster'] == i, 1],
                macsto[macro_stocks_df['cluster'] == i, 2], s=50, c=color_list[i])


fig = plt.figure()
ax = plt.axes(projection='3d')
for i in range(num):
    ax.scatter3D(macsto[macro_stocks_df['cluster'] == i, 0], macsto[macro_stocks_df['cluster']
                                                                    == i, 1], macsto[macro_stocks_df['cluster'] == i, 2], c=color_list[i])

# histogram plots for monthly returns within each cluster

for i in range(num):
    mchange = cluster_list[i]['monthly_return'].to_list()
    plt.figure()
    plt.hist(mchange, bins=10, label=i)
    plt.legend()
    print(i, cluster_list[i]['monthly_return'].describe())


# Output: predict a range of likely stock market monthly return for the following month, given the macroeconomic environment, as described by clustering

# print(macro_stocks_df)

# current month
ts = pd.Timestamp('2022-08-01')
# find the timestamp for three months(a quarter) ago
ts2 = ts - DateOffset(months=3)

prediction_range_list = []
for c in cluster_list:
    monthly_return_range = [
        c['monthly_return'].min(), c['monthly_return'].max()]
    average_monthly_return_range = [
        c['avg_monthly_return'].min(), c['avg_monthly_return'].max()]
    prediction_range_list.append(
        (monthly_return_range, average_monthly_return_range))


def stock_prediction_from_macro_clustering(t, cluster_list, prediction_range_list):
    for i in range(0, num):
        c = cluster_list[i]
        r = prediction_range_list[i]
        for d in c['observation_date']:
            if ts2 == d:
                return r


stock_prediction_from_macro_clustering(
    ts2, cluster_list, prediction_range_list)
