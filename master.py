# Created by Ivan Struk @ Morpher

import yfinance as yf
import pandas as pd
import numpy as np
import requests
from matplotlib import pyplot as plt
import datetime
import csv
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from def_data import spy, qqq

all_markets = spy() + qqq()
print(all_markets)

"""  These are the history modules. They pull data from Yahoo Finance
     and also handle most of the calculations.
"""

def get_hist(symbol):
    target_tickers = []
    target_tickers.append(symbol)
    fetch = yf.download(tickers = target_tickers,
                period = "5y",
                interval = "1d",
                group_by = "ticker",
                auto_adjust = False,
                prepost = True,
                treads = True,
                proxy = None)
    df = pd.DataFrame(data=fetch, index=None).reset_index(drop=False)
    df["Pre-Market Change"] = df["Open"] - df["Close"].shift(+1)
    df["Intraday Change"] = df["Close"] - df["Open"]
    df["Total Daily Change"] = df["Intraday Change"] + df["Pre-Market Change"]
    df["Pre-Market R%"] = round(((df["Pre-Market Change"] / df["Close"].shift(+1))*100),2)
    df["Intraday R%"] = round(((df["Intraday Change"] / df["Open"])*100),2)
    df["Total Daily R%"] = round((df["Pre-Market R%"] + df["Intraday R%"]),2)
    df["PM Price Action Share"] = round(df["Pre-Market R%"]/df["Total Daily R%"],2)
    df["% Daily Change Att PreM"] = df["Pre-Market Change"] / df["Total Daily Change"]
    df["ABS PM Chn"] = df["Pre-Market Change"].abs()
    df["ABS ID Chn"] = df["Intraday Change"].abs()
    df["ABS ID + PM"] = df["ABS ID Chn"] + df["ABS PM Chn"]
    df["ABS PM CHN / ABS ID + PM"] = round((df["ABS PM Chn"] / df["ABS ID + PM"]),2) # this is a good one
    df["Intraday HL Range"] = df["High"] - df["Low"]
    df1 = df.iloc[1:]
    return df1
    
def hunt_hist(symbol):
    target_tickers = []
    target_tickers.append(symbol)
    fetch = yf.download(tickers = target_tickers,
                period = "5y",
                interval = "1d",
                group_by = "ticker",
                auto_adjust = False,
                prepost = True,
                treads = True,
                proxy = None)
    df = pd.DataFrame(data=fetch, index=None).reset_index(drop=False)
    df["Pre-Market Change"] = df["Open"] - df["Close"].shift(+1)
    df["Intraday Change"] = df["Close"] - df["Open"]
    df["Premarket D"] = np.where(df['Pre-Market Change']>0, 2, 1)
    df["Intraday D"] = np.where(df['Intraday Change']>0, 2, 1)
    df["H: Both True"] = df["Intraday D"] + df["Premarket D"]
    df["H1: Increasing"] = np.where(df["H: Both True"] == 4, 1, 0)
    df["H2: Decreasing"] = np.where(df["H: Both True"] == 2, 1, 0)
    df["H: Both True"] = df["Intraday D"] + df["Premarket D"]
    df["H1: Increasing"] = np.where(df["H: Both True"] == 4, 1, 0)
    df["H2: Decreasing"] = np.where(df["H: Both True"] == 2, 1, 0)
    df["Pre-Market D+"] = np.where(df['Pre-Market Change']>0, 1, 0)
    df["Intraday D+"] = np.where(df['Intraday Change']>0, 1, 0)
    df["Pre-Market D-"] = np.where(df['Pre-Market Change']<0, 1, 0)
    df["Intraday D-"] = np.where(df['Intraday Change']<0, 1, 0)
    df["Temp Calc"] = df["Pre-Market D+"]+df["Intraday D+"]
    df["Temp Calc1"] = np.where(df['Temp Calc']>1, 1, 0)
    df = df.drop(axis=1, labels = ["Temp Calc", 
                                   "H: Both True", 
                                   "H1: Increasing", 
                                   "H2: Decreasing", 
                                   "Premarket D", 
                                   "Intraday D"])
    df3 = df.iloc[1:]
    return df3



"""  Below are the various tests that can be executed. 
"""


def test_sample_contribution(symbol):
    stocks = symbol
    stock_names = []
    premarket_att = []
    
    print("Crunching numbers ... (this may take a while)")
    for i in stocks:
        df_sub = pd.DataFrame(get_hist(i))
        df = df_sub.fillna(value=0)
        result = sum(df["ABS PM CHN / ABS ID + PM"])/len(df["ABS PM CHN / ABS ID + PM"])
        name = i
        stock_names.append(name)
        premarket_att.append(result)
        
    stock_parser = {
        "Symbol" : [],
        "Result" : []
    }
    results_df = pd.DataFrame(stock_parser)
    results_df["Symbol"] = stock_names
    results_df["Result"] = premarket_att
    label = "Premarket trading as % of daily action"
    print("Saving to csv...")
    results_df.to_csv("{}.csv".format(label))
    print("Result:")
    
    average_premarket_weight = sum(results_df["Result"])/len(results_df["Result"])
    print("On average premarket trading contributes to ",
          (round(average_premarket_weight,2)*100), 
          "% of daily price action within the selected sample.")
    

def test_sample_indication(symbol):
    stock_names = []
    results = []
    stocks = symbol
    print("This may take a while if you have defined a large number of stocks")
    
    for i in stocks:
        df = pd.DataFrame(get_hist(i))
        #df = df_sub.fillna(value=0)
        result = round((sum(df["H: Both True"]))/(len(list(df["H: Both True"]))),4)
        name = i
        #print(name, result)
        stock_names.append(name)
        results.append(result)
        
    stock_parser = {
        "Symbol" : [],
        "Result" : []
    }
    results_df = pd.DataFrame(stock_parser)
    results_df["Symbol"] = stock_names
    results_df["Result"] = results
    label = "A stock increasing or decreasing in value during premarket has an X probability of maintaining direction"
    print("Saving to csv...")
    results_df.to_csv("{}.csv".format(label))
    print("Result:")
    
    
    final_result = sum(results_df["Result"])/len(results_df["Result"])
    print("A stock increasing or decreasing in value during premarket has a ",
          (round(final_result,2)*100), 
          "% probability of maintaining price action in the same direction.")
    
def test_sample_long(symbol):
    stocks = symbol
    stock_names = []
    results = []
    
    print("This may take a while if you have defined a large number of stocks")
    
    for i in stocks:
        df = pd.DataFrame(hunt_hist(i))
        #df = df_sub.fillna(value=0)
        result = round((sum(df["Temp Calc1"]))/(sum(df["Pre-Market D+"])),4)
        name = i
        #print(name, result)
        stock_names.append(name)
        results.append(result)
        
    stock_parser = {
        "Symbol" : [],
        "Result" : []
    }
    results_df = pd.DataFrame(stock_parser)
    results_df["Symbol"] = stock_names
    results_df["Result"] = results
    label = "A stock increasing in value during premarket has an X probability of further gain"
    print("Saving to csv...")
    results_df.to_csv("{}.csv".format(label))
    print("Result:")
    
    final_result = sum(results_df["Result"])/len(results_df["Result"])
    print("A stock increasing in value during premarket has a ",
          (round(final_result,2)*100), 
          "% probability of further increasing in intraday.")


