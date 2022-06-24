In this ongoing Python data project, we study more than half of a century of stock market and macroeconomic data(from 1940s to the present, including the COVID-19 pandemic), with the hope of understanding their relationships better. So far we have explored S&P 500 data as well as unemployment and inflation rates, a pair of macroeconomic indicators with interesting connections historically. Numerous plots were generated to visualize our data. 

In particular, by the K-Means Clustering Machine Learning algorithm, we divided the two-dimensional(normalized or standardized unemployment and inflation rates) data into three economically interesting clusters: low inflation - low unemployment, high inflation - low unemployment and low inflation - high unemployment. Some other numbers of clusters also seem interesting statistically. 

To gain insights towards stock prices through macroeconomic indicators, we first tried to run linear regression(over many different time periods and clusters), with the macroeconomic indicators being the dependent variables. However, this model turned out to be utterly wrong. Next we plan to just divide the stock market data according to the macroeconomic clusters, and directly study their statistics in each cluster. 

One interesting statistical discovery was made! We hypothesized that the waiting time for changing clusters (For instance, during the course of the COVID-19 pandemic, the economy moved from the low inflation - low unemployment cluster, to the low inflation - high unemployment cluster, and then to the high inflation - low unemployment cluster) is of the Geometric distribution, and decided not to reject our hypothesis as the result of our hypothesis testing (large p-values). This waiting time(as a random variable) is related to the lengths of business cycles. 

A good understanding of the clustering behavior of macroeconomic indicators gives us insights about the changes of our macroeconomic climates. 




