# Macroeconomics and Business Cycles Predictor 

This ongoing Python project analyzes over half a century of macroeconomic data (from the 1940s to the present, including the COVID-19 pandemic) to better understand changes in macroeconomic conditions and business cycles. Our analysis currently focuses on two key indicators: unemployment and inflation rates, which have historically shown interesting relationships. We've generated various plots to visualize the data and uncover patterns.
Using the K-Means Clustering algorithm, we’ve categorized the normalized unemployment and inflation data into three key clusters:
    • Low inflation, low unemployment
    • High inflation, low unemployment
    • Low inflation, high unemployment
Other clustering configurations also reveal statistically interesting groupings. These clusters are visualized to provide a clearer understanding of macroeconomic shifts.

![3 clusters](https://github.com/elainechowqz/Macroeconomics-and-Markets/blob/master/macro_and_stocks/3_clusters.png)

One interesting statistical discovery is made! We hypothesize that the waiting time for changing macroeconomic clusters/time interval between consecutive cluster changes (For instance, during the course of the COVID-19 pandemic, the economy moved from low inflation - low unemployment, to low inflation - high unemployment, and then to high inflation - low unemployment) is of the Geometric distribution (or the Exponential distribution if we assume that time is continuous), and decide not to reject our hypothesis due to very large P-values. This time interval (as a random variable) is related to the lengths of business cycles and how long our macroeconomic environments last. A good understanding of the clustering behavior of macroeconomic indicators gives us insights about the changes of our macroeconomic climates and business cycles. 

Finally, to gain insights towards stock prices through macroeconomic indicators, we look at stock prices in different macroeconomic clusters, and help make predictions. 

Outputs: 
1. Based on the statistical/machine learning discovery described above, this program helps predict/quantify when and how likely the macroeconomic environment is going to change; 
2. This program helps predict the stock market by returning an estimated interval of future monthly returns, based on historical data in idential or similar macroeconomic clusters. 








