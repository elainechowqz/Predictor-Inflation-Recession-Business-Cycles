# Macroeconomics and Markets

In this ongoing Python data project, we study more than half of a century of stock market and macroeconomic data(from 1940s to the present, including the COVID-19 pandemic), with the hope of understanding their relationships better. So far we have explored S&P 500 data as well as unemployment and inflation rates, a pair of macroeconomic indicators with interesting connections historically. Numerous plots were generated to visualize our data. 

In particular, by the K-Means Clustering Machine Learning algorithm, we divided the two-dimensional(normalized or standardized unemployment and inflation rates) data into three economically interesting clusters: low inflation - low unemployment, high inflation - low unemployment and low inflation - high unemployment. Some other numbers of clusters also seem interesting statistically. 

One interesting statistical discovery was made! We hypothesized that the waiting time for changing macroeconomic clusters (For instance, during the course of the COVID-19 pandemic, the economy moved from low inflation - low unemployment, to low inflation - high unemployment, and then to high inflation - low unemployment) is of the Geometric distribution(or the Exponential distribution if we assume that time is continuous), and decided not to reject our hypothesis as the result of our hypothesis testing (large p-values). This waiting time(as a random variable) is related to the lengths of business cycles and our macroeconomic environment. 

A good understanding of the clustering behavior of macroeconomic indicators gives us insights about the changes of our macroeconomic climates and business cycles. 

To gain insights towards stock prices through macroeconomic indicators, we first tried to run linear regression(over many different time periods and clusters), with the macroeconomic indicators being the dependent variables. However, the R^2 values are really low, showing that linear regression is not a good model here. Therefore, we next explore the statistical associations between stock market returns and macroeconomic indicators from other angles. 

Final outputs: 
1. Based on the statistical/machine learning discovery described above, this program helps predict/quantify when and how likely the macroeconomic environment is going to change; 
2. This program serves as a stock market predictor for the current or future months, by returning an estimated interval of monthly returns, based on historical data in idential or similar macroeconomic clusters. 








