# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 

@author: Ivan Struk

"""

import yfinance as yf
import pandas as pd
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


"""  Markets
"""

def spy():
    spy_1 = pd.read_csv("d_SP500.csv", encoding = "utf-8", usecols= ["Symbol"])
    spy_list = spy_1["Symbol"]
    real_spy_list = list(spy_list)
    spy = real_spy_list
    return spy

def qqq():
	qqq_1 = pd.read_csv("d_Nasdaq100.csv")
	qqq_list = qqq_1["Ticker"]
	real_qqq_list = list(qqq_list)
	qqq = real_qqq_list
	return qqq


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
    df["ABS PM CHN / ABS ID + PM"] = round((df["ABS PM Chn"] / df["ABS ID + PM"]),2)
    df["Intraday HL Range"] = df["High"] - df["Low"]
    df1 = df.iloc[1:]
    return df1

def get_hist2(symbol):
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
    df["Premarket D"] = np.where(df['Pre-Market Change']>0, "Up", "Down")
    df["Intraday D"] = np.where(df['Intraday Change']>0, "Up", "Down")
    df["H: Both True"] = np.where(df['Intraday D'] == df["Premarket D"], 1, 0)
    df2 = df.iloc[1:]
    return df2


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
   
    df3 = df.iloc[1:]
    return df3

