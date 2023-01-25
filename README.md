# Macroeconomics and Markets

In this ongoing Python data project, we study more than half of a century of stock market and macroeconomic data(from 1940s to the present, including the COVID-19 pandemic), with the hope of understanding their relationships better. So far we have explored S&P 500 data as well as unemployment and inflation rates, a pair of macroeconomic indicators with interesting connections historically. Numerous plots are generated to visualize our data. 

In particular, by the K-Means Clustering Machine Learning algorithm, we divide the two-dimensional(normalized or standardized unemployment and inflation rates) data into three economically interesting clusters: low inflation - low unemployment, high inflation - low unemployment and low inflation - high unemployment. Some other numbers of clusters also seem interesting statistically. Clusters are visualized. 

![3 clusters](https://github.com/elainechowqz/Macroeconomics-and-Markets/blob/master/macro_and_stocks/3_clusters.png)

One interesting statistical discovery is made! We hypothesize that the waiting time for changing macroeconomic clusters/time interval between consecutive cluster changes(For instance, during the course of the COVID-19 pandemic, the economy moved from low inflation - low unemployment, to low inflation - high unemployment, and then to high inflation - low unemployment) is of the Geometric distribution(or the Exponential distribution if we assume that time is continuous), and decide not to reject our hypothesis due to very large P-values. This time interval(as a random variable) is related to the lengths of business cycles and how long our macroeconomic environments last. A good understanding of the clustering behavior of macroeconomic indicators gives us insights about the changes of our macroeconomic climates and business cycles. 

Finally, to gain insights towards stock prices through macroeconomic indicators, we look at stock prices in different macroeconomic clusters, and help make predictions. 

Outputs: 
1. Based on the statistical/machine learning discovery described above, this program helps predict/quantify when and how likely the macroeconomic environment is going to change; 
2. This program helps predict the stock market by returning an estimated interval of future monthly returns, based on historical data in idential or similar macroeconomic clusters. 








