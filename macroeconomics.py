import pandas as pd
import pandas_datareader as pdr
import datetime 
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats 
import statsmodels.api as sm
from sklearn.cluster import KMeans

# We use normalized data in this Python document. 

# Retrieve CPI and Unemployment data. Standardize the data for analysis.

CPI_df = pd.read_excel (r'') # enter the filepath for the CPI data file 
Unemployment_df = pd.read_excel (r'') # enter the filepath for the Unemployment data file

Inflation_Unemploymt_df = pd.merge(CPI_df, Unemployment_df, on='observation_date')

Inflation_Unemploymt_df['Unemployment Rate Normalized'] = (Inflation_Unemploymt_df['Unemployment Rate'] -Inflation_Unemploymt_df['Unemployment Rate'].min())/(Inflation_Unemploymt_df['Unemployment Rate'].max() -Inflation_Unemploymt_df['Unemployment Rate'].min())

Inflation_Unemploymt_df['Monthly Inflation Rate'] = ((Inflation_Unemploymt_df['CPI']/ Inflation_Unemploymt_df['CPI'].shift(1)) -1)*100
Inflation_Unemploymt_df['Annual Inflation Rate'] = ((Inflation_Unemploymt_df['CPI']/ Inflation_Unemploymt_df['CPI'].shift(12)) -1)*100

Inflation_Unemploymt_df['Annual Inflation Rate Normalized'] = (Inflation_Unemploymt_df['Annual Inflation Rate'] -Inflation_Unemploymt_df['Annual Inflation Rate'].min())/(Inflation_Unemploymt_df['Annual Inflation Rate'].max() -Inflation_Unemploymt_df['Annual Inflation Rate'].min())

# Create scatter plots for inflation and unemployment rates during different time periods 

Inflation_Unemploymt_df.plot.scatter(x='Unemployment Rate', y='Annual Inflation Rate')

def period_scatter_plot(d1, d2, df):
    new_df = df.loc[(df['observation_date'] >= d1) & (df['observation_date'] <= d2)]
    new_df.plot.scatter(x='Unemployment Rate', y='Annual Inflation Rate')
    
period_list = [['1949-01-01', '1959-12-01'], ['1960-01-01', '1969-12-01'], ['1970-01-01', '1979-12-01'], ['1980-01-01', '1989-12-01'], ['1990-01-01', '1999-12-01'], ['2000-01-01', '2009-12-01'], ['2010-01-01', '2020-10-01']]

for i in range(len(period_list)):
    period_scatter_plot(period_list[i][0], period_list[i][1], Inflation_Unemploymt_df)
    
# Clustering

#Create a Numpy array for the inflation-unemployment dataframe above from 1949 onwards
Inflation_Unemploymt_df2 = Inflation_Unemploymt_df[12:]
Inf_Unem = Inflation_Unemploymt_df2[['Unemployment Rate Normalized', 'Annual Inflation Rate Normalized']].to_numpy()

#Run K-Means Clustering through Scikit-Learn
# There are three economically interesting clusters: high inflation + low unemployment rate, low inflation + high unemployment rate, and low inflation + low unemployment rate
num = 3

km = KMeans(n_clusters=num, random_state=0).fit(Inf_Unem)
l_km = km.labels_
c_km = km.cluster_centers_

# Plot different clusters

color_list = ['green', 'red', 'yellow', 'purple', 'pink', 'orange', 'cyan', 'lightgreen', 'olive']

plt.figure()

for i in range(num):
    plt.scatter(Inf_Unem[l_km == i, 0], Inf_Unem[l_km == i, 1], s = 50, c = color_list[i], label = i)
    
# Plot all the centroids
plt.scatter(c_km[:, 0], c_km[:, 1], s = 250, c = 'blue', marker = '*', label = 'centroids')

plt.legend(scatterpoints = 1)
plt.grid()
plt.xlabel('Unemployment Rate Normalized')
plt.ylabel('Annual Inflation Rate Normalized')

# Add a cluster label column to the orginal dataframe 
Inflation_Unemploymt_df2['cluster'] = l_km

# Create a list of dataframes corresponding to all the clusters, and a bunch of histograms for the years in each cluster
cluster_list = []

for i in range(num):
    cluster_df = Inflation_Unemploymt_df2.loc[Inflation_Unemploymt_df2['cluster'] == i]
    cluster_list.append(cluster_df)
    timedf = cluster_df['observation_date']
    plt.figure()
    timedf.groupby([timedf.dt.year]).count().plot(kind="bar", label = i)
    plt.legend()
    
# Create a list of dates when the cluser changes    

change_cluster_dates = []
Inflation_Unemploymt_df2['cluster change'] = Inflation_Unemploymt_df2['cluster'] - Inflation_Unemploymt_df2['cluster'].shift(1)

for index, row in Inflation_Unemploymt_df2[1:].iterrows():
    if row['cluster change'] != 0:
        change_cluster_dates.append([index, row['observation_date']])

# Create a list of continuous time intervals within individual clusters

cluster_time_intervals_months = []
cluster_time_intervals_days = []

for i in range(1, len(change_cluster_dates)):
    diff = (change_cluster_dates[i][1] - change_cluster_dates[i - 1][1]).days
    cluster_time_intervals_days.append(diff)
    cluster_time_intervals_months.append(change_cluster_dates[i][0] - change_cluster_dates[i - 1][0])
    
plt.figure()
plt.hist(cluster_time_intervals_months, bins=10, label = 'Cluster Time Intervals Months')
plt.legend()

# Test if the histograms plotted above indeed agree with the exponential distribution

min_month_change = min(cluster_time_intervals_months)
max_month_change = max(cluster_time_intervals_months)
mean_month_change = np.mean(cluster_time_intervals_months)

# Get an exponential random variable and a geometric random variable with the same parameters

# exponential distribution
rv = scipy.stats.expon(min_month_change, mean_month_change)

# geometric distribution
rv2 = scipy.stats.geom(1/mean_month_change)

# chisqure test for categorical data (exponential and geometric distributions)
bins = plt.hist(cluster_time_intervals_months, bins=10)[1]
observations = plt.hist(cluster_time_intervals_months, bins=10)[0]
ob = np.asarray(observations)

expectations1 = []
expectations2 = []

for i in range(1, len(bins) - 1):
    expectation1 = (rv.cdf(bins[i]) - rv.cdf(bins[i - 1]))*len(cluster_time_intervals_months)
    expectations1.append(expectation1)
    expectation2 = (rv2.cdf(bins[i]) - rv2.cdf(bins[i - 1]))*len(cluster_time_intervals_months)
    expectations2.append(expectation2)
last1 = len(cluster_time_intervals_months) - sum(expectations1)
last2 = len(cluster_time_intervals_months) - sum(expectations2)
expectations1.append(last1)
expectations2.append(last2)
    
ex1 = np.asarray(expectations1)
ex2 = np.asarray(expectations2)

chisq1, p1 = scipy.stats.chisquare(ob, ex1)
print(p1)

chisq2, p2 = scipy.stats.chisquare(ob, ex2)
print(p2)

