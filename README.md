# Macroeconomics and Business Cycles Predictor 

This ongoing Python project analyzes over half a century of macroeconomic data (from the 1940s to the present, including the COVID-19 pandemic) to better understand changes in macroeconomic conditions and business cycles. Our analysis currently focuses on two key indicators: unemployment and inflation rates, which have historically shown interesting relationships. We've generated various plots to visualize the data and uncover patterns.

Using the K-Means Clustering algorithm, we’ve categorized the normalized unemployment and inflation data into three key clusters:

    • Low inflation, low unemployment
    
    • High inflation, low unemployment
    
    • Low inflation, high unemployment
    
Other clustering configurations also reveal statistically interesting groupings. These clusters are visualized to provide a clearer understanding of macroeconomic shifts.

![3 clusters](https://github.com/elainechowqz/Macroeconomics-and-Markets/blob/master/macro_and_stocks/3_clusters.png)

Key Discovery

We uncovered that changes in macroeconomic conditions (represented by shifts in unemployment and inflation) follow a Markov process. Through hypothesis testing, we found that the time between transitions from one cluster to another (e.g., from "low inflation, low unemployment" to "low inflation, high unemployment" during the COVID-19 pandemic) follows a Geometric distribution (or Exponential distribution in continuous time). This time interval correlates with business cycle lengths and the duration of various macroeconomic environments.
Understanding these transitions helps predict shifts in macroeconomic climates and business cycles.

Finally, to gain insights towards stock prices through macroeconomic indicators, we look at stock prices in different macroeconomic clusters, and help make predictions. 

Outputs

    1. Macroeconomic Environment Prediction
The model predicts the timing and likelihood of macroeconomic shifts and provides insights into the duration of business cycles. This has potential applications to business planning. 

    2. Future Predictions
Given the strong ties between macroeconomic indicators and other financial measures (e.g., market and credit risk), this project opens up the possibility of extending the analysis to areas like financial risk management:

        ◦ Stock market returns under different macroeconomic conditions
        
        ◦ Regression models between macroeconomic indicators and credit default probabilities, with applications in predicting credit risks








