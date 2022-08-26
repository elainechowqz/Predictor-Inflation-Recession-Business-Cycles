import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import statsmodels.api as sm
from sklearn.cluster import KMeans
import pandas as pd

# Get inflation and unemployment data

CPI_df = pd.read_excel(r"/.../CPIAUCSL.xls", skiprows=10)
CPI_df.columns = ["observation_date", "CPI"]

Unemployment_df = pd.read_excel(r"/.../UNRATE.xls", skiprows=10)
Unemployment_df.columns = ["observation_date", "Unemployment Rate"]

CPI_df["Annual Inflation Rate"] = ((CPI_df["CPI"] / CPI_df["CPI"].shift(12)) - 1) * 100

Inflation_Unemploymt_df = pd.merge(CPI_df[12:], Unemployment_df, on="observation_date")

# Standardize data

Unemployment_mean = Inflation_Unemploymt_df["Unemployment Rate"].mean()
Unemployment_std = Inflation_Unemploymt_df["Unemployment Rate"].std()

Inflation_Unemploymt_df["Unemployment Rate Standardized"] = (
    Inflation_Unemploymt_df["Unemployment Rate"] - Unemployment_mean
) / (Unemployment_std)

AnnualInf_mean = Inflation_Unemploymt_df["Annual Inflation Rate"].mean()
AnnualInf_std = Inflation_Unemploymt_df["Annual Inflation Rate"].std()

Inflation_Unemploymt_df["Annual Inflation Rate Standardized"] = (
    Inflation_Unemploymt_df["Annual Inflation Rate"] - AnnualInf_mean
) / (AnnualInf_std)

# Scatter plots of Annual Inflation rates and Unemployment rates during different time periods

Inflation_Unemploymt_df.plot.scatter(x="Unemployment Rate", y="Annual Inflation Rate")


def period_scatter_plot(d1, d2, df):
    new_df = df.loc[(df["observation_date"] >= d1) & (df["observation_date"] <= d2)]
    new_df.plot.scatter(x="Unemployment Rate", y="Annual Inflation Rate")


period_list = [
    ["1949-01-01", "1959-12-01"],
    ["1960-01-01", "1969-12-01"],
    ["1970-01-01", "1979-12-01"],
    ["1980-01-01", "1989-12-01"],
    ["1990-01-01", "1999-12-01"],
    ["2000-01-01", "2009-12-01"],
    ["2010-01-01", "2020-10-01"],
]

for i in range(len(period_list)):
    period_scatter_plot(period_list[i][0], period_list[i][1], Inflation_Unemploymt_df)

# Clustering data and visualize

# Create a Numpy array for the inflation-unemployment dataframe above

Inflation_Unemploymt_df2 = Inflation_Unemploymt_df
Inf_Unem = Inflation_Unemploymt_df2[
    ["Unemployment Rate Standardized", "Annual Inflation Rate Standardized"]
].to_numpy()

# Run K-Means Clustering

# num = 4
# num = 6
num = 3

km = KMeans(n_clusters=num, random_state=0).fit(Inf_Unem)
l_km = km.labels_
c_km = km.cluster_centers_

# Plot different clusters

color_list = [
    "green",
    "red",
    "yellow",
    "purple",
    "pink",
    "orange",
    "cyan",
    "lightgreen",
    "olive",
]

plt.figure()

for i in range(num):
    plt.scatter(
        Inf_Unem[l_km == i, 0], Inf_Unem[l_km == i, 1], s=50, c=color_list[i], label=i
    )

# Plot all the centroids

plt.scatter(c_km[:, 0], c_km[:, 1], s=250, c="blue", marker="*", label="centroids")

plt.legend(scatterpoints=1)
plt.grid()
plt.xlabel("Unemployment Rate Standardized")
plt.ylabel("Annual Inflation Rate Standardized")

# Add a cluster label column to the orginal dataframe
Inflation_Unemploymt_df2["cluster"] = l_km

# Create a list of dataframes corresponding to all the clusters, 
# and a bunch of histograms for the years in each cluster

cluster_list = []

for i in range(num):
    cluster_df = Inflation_Unemploymt_df2.loc[Inflation_Unemploymt_df2["cluster"] == i]
    cluster_list.append(cluster_df)
    timedf = cluster_df["observation_date"]
    plt.figure()
    timedf.groupby([timedf.dt.year]).count().plot(kind="bar", label=i)
    plt.legend()

# Create a list of dates when the cluser changes

change_cluster_dates = []
Inflation_Unemploymt_df2["cluster change"] = Inflation_Unemploymt_df2[
    "cluster"
] - Inflation_Unemploymt_df2["cluster"].shift(1)

for index, row in Inflation_Unemploymt_df2[1:].iterrows():
    if row["cluster change"] != 0:
        change_cluster_dates.append([index, row["observation_date"]])

# Create a list of continuous time intervals within individual clusters

cluster_time_intervals_months = []
cluster_time_intervals_days = []

for i in range(1, len(change_cluster_dates)):
    diff = (change_cluster_dates[i][1] - change_cluster_dates[i - 1][1]).days
    cluster_time_intervals_days.append(diff)
    cluster_time_intervals_months.append(
        change_cluster_dates[i][0] - change_cluster_dates[i - 1][0]
    )

plt.figure()
plt.hist(cluster_time_intervals_months, bins=10, label="Cluster Time Intervals Months")
plt.legend()


# Hypothesis Testing
# Null hypothesis: the time interval between macroeconomic cluster 
# changes is of exponential(if we treat time as continuous) or 
# geometric(if we treat time as discrete, e.g. number of months) distribution

min_month_change = min(cluster_time_intervals_months)
max_month_change = max(cluster_time_intervals_months)
mean_month_change = np.mean(cluster_time_intervals_months)

# Get an exponential random variable and a geometric random 
# variable based on parameters derived from data

# exponential distribution
rv = scipy.stats.expon(min_month_change, mean_month_change)
# geometric distribution
rv2 = scipy.stats.geom(1 / mean_month_change)

# chisqure test for categorical data (exponential and geometric distributions)
bins = plt.hist(cluster_time_intervals_months, bins=10)[1]
observations = plt.hist(cluster_time_intervals_months, bins=10)[0]
ob = np.asarray(observations)

expectations1 = []
expectations2 = []

for i in range(1, len(bins) - 1):
    expectation1 = (rv.cdf(bins[i]) - rv.cdf(bins[i - 1])) * len(
        cluster_time_intervals_months
    )
    expectations1.append(expectation1)
    expectation2 = (rv2.cdf(bins[i]) - rv2.cdf(bins[i - 1])) * len(
        cluster_time_intervals_months
    )
    expectations2.append(expectation2)
last1 = len(cluster_time_intervals_months) - sum(expectations1)
last2 = len(cluster_time_intervals_months) - sum(expectations2)
expectations1.append(last1)
expectations2.append(last2)

ex1 = np.asarray(expectations1)
ex2 = np.asarray(expectations2)

# P value for hypothesis testing involving the exponential distribution
chisq1, p1 = scipy.stats.chisquare(ob, ex1)
print(p1)

# P value for hypothesis testing involving the geometric distribution
chisq2, p2 = scipy.stats.chisquare(ob, ex2)
print(p2)
