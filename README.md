In this ongoing data project, we study more than half of a century of stock market and macroeconomic data(from 1940s to the present, including the COVID-19 pandemic), with the hope of understanding their relationships better. So far we have explored S&P 500 data as well as unemployment and inflation rates, a pair of macroeconomic indicators with interesting connections historically. Numerous plots were generated to visualize our data. 

In particular, by the K-Means Clustering algorithm, we divided the two-dimensional(normalized or standardized unemployment and inflation rates) data into three economically interesting clusters: low inflation - low unemployment, high inflation - low unemployment and low inflation - high unemployment. 

To gain insights about stock prices through macroeconomic indicators, we first tried to run linear regression(over many different time periods and clusters), with the macroeconomic indicators being the dependent variables. However, this model turned out to be utterly wrong. Next we plan to just divide the stock market data according to the macroeconomic clusters, and directly study their statistics in each cluster. 

One interesting statistical discovery was made! We hypothesized that the waiting time for changing clusters (e.g. when the COVID-19 pandemic hit, the economy moved from the low inflation - high unemployment cluster to the low inflation - high unemployment cluster) is of the Geometric distribution, and found very strong statistical evidences for it. 

A good understanding of the clustering behavior of macroeconomic indicators gives us insights about the changes of our macroeconomic climates. It would be useful for learning about not only the markets, but also many other factors like business cycles. 




