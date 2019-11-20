# Backtesting Pre-Market Price Action
This allows you to determine whether certain stocks of the S&P500 exchibit an indicative price-action or not, and examines how the same stocks move during earnings report periods. 

A considerable amount of stock market price action is attributable to the extended-hours trading sessions. While most people think of the regular trading hours (9:30 - 16:00) when they think of trading, pre-market and after-hours trading is extremely important, especially given the accesibility of ECNs with brokers nowadays. Often when investors start examining the pre-market with more attention they start asking themselves things like "if this stock is going up now in pre-market, should I buy it ? Will it keep going up through the day (intraday) ?", and it's something I wanted to determine as well. 

The code I provide may not be entirely Pythonic, however it is a means to an end in determining the answer to a series of extended trading hours questions that I, my colleagues, and many others have had and will continue to have. 

## The Sessions

Before diving in, I want to explain how I view premarket and afterhours. 
![Visualisation of premarket and after-hours sessions](https://i.imgur.com/tj5vXK4.png)

This is how a trading day looks like. Pre-market trading begins at 4:00 and lasts until 9:30, then the market opens to all participants (this session is referred to as the intraday), and when it closes at 16:00 the after-hours session begins, lasting until 20:00. At 20:00 all markets close, and there is no trading until 4:00 the next day. 

This leaves you with two ways of thinking about these unorthodox trading sessions. 
a) You can think of the main trading session surrounded by two extended sessions, the pre and post (after). Which means you examine price-action seperately by three sessions. 

or

b) You can think of the extended trading hours sessions as one large pre-market. 

I choose the latter, because I believe it is more in-line with principles of the post-announcement drift, and on practical level it's what has always made more sense to me. 

In examining the "pre-market" session, I refer to the price action that occurs **between the close and the next day's open**. This means we consider the price action from when the market closes at 16:00 until it opens the next day at 9:30. This works because institutional sentiment carries over night, and this is the period in which all reporting is done. 

## The Code

The code is broken apart into three .py modules. 
**tests_main.py**: contains the consolidated functions for executing the tests.
**EOD_parser.py**: contains the functions associated with fetching historical price data. 
**earnings_parser.py**: contains functions that scrape the SEC EDGAR database for earnings dates. 

In addition there are two CSV files that contain lists of stock symbols. 

Finally, **master_premarket_tests** is a Jupyter Notebook containing all of the tests in a nice and presentable way. 
From the notebook you can explore the data, output the dataframes in whatever format you need, and change the sampled stocks. 

Tests: 
Function | Application 
------------ | ------------- 
test_sample_contribution(symbol) | Here we determine how much of total close-to-close price action is attributable to the pre-market.
test_sample_long(symbol) | Now we test whether a stock that increases during pre-market keeps increasing during intraday. 
test_sample_indication(symbol) | This is a test of the overall persistence. Is pre-market action indicative of what occurs during the intraday. 
test_sample_earnings(symbol) | Finally, this function runs a series of similar tests, but only for the period directly following an earnings announcement. 


## Dependencies

While this code isn't so robust, there are a lot of different moving parts.
- Numpy
- Pandas
- YFinance
- BeautifulSoup
- RegEx

## Feedback

If you have any feedback, I would love to improve this repository, shoot me an email: ivan.s@eastmillcapital.com 
This was originally created as part of an investigation intp pre-market price action while working at Morpher.
If you're interested in a blockchain trading platform that supports 24/7 trading (not just pre-market), and no fees or commisions, definitely check out [Morpher](https://morpher.com). 
