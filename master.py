# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 

@author: Ivan Struk

"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests

import datetime

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import bs4
import re


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


def getDateList(ticker):
    print('Searching for earnings report dates for '+ticker)
    url_p_1 = "https://www.sec.gov/cgi-bin/"
    url_p_2 = "browse-edgar?type=10-&dateb=&owner=include&count=100&"
    url_p_3 = 'action=getcompany&CIK=%s'
    url_ag = url_p_1 + url_p_2 + url_p_3
    url =  url_ag % ticker
    headerInfo={'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url,headers=headerInfo)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    noMatch = soup.select('p > center > h1')
    trElems = soup.select('tr')
    '''Regex to get earnings report dates no earlier than 1/1/2000'''
    dateFind = re.compile(r'2\d{3}-\d{2}-\d{2}')
    if noMatch != []:
        print('Could not find earnings report dates for '+ticker)
        return None
    dateList = []
    dateList.append(['EarningsDates'])
    for tr in trElems:
        tdElems = tr.select('td')
        if len(tdElems) == 5 and dateFind.search(tdElems[3].getText()) != None:
            date = tdElems[3].getText()
            converted1 = datetime.datetime.strptime(date,'%Y-%m-%d')
            converted = converted1.strftime('%m/%d/%Y')
            dateList.append([converted])
    return dateList

def getEarnings(ticker, header=True):
    ticker = ticker
    dateList = getDateList(ticker)
    df = pd.DataFrame(dateList)
    df = df.iloc[1:]
    return df



def give_df(symbol):
    x = symbol
    def get_er(x):
        df_target = getEarnings(x)
        df_target["Date"] = df_target[0]
        df_target = df_target.drop(0, axis = 1)
        df_target["Date"] = pd.to_datetime(df_target["Date"], format = "%Y-%m-%d")
        df_target["Event"] = "Earnings"
        df_er = df_target
        return df_er
    
    def fetch_history(x):
        target_tickers = []
        target_tickers.append(x)
        fetch = yf.download(tickers = target_tickers,
                    period = "5y",
                    interval = "1d",
                    group_by = "ticker",
                    auto_adjust = False,
                    prepost = True,
                    treads = True,
                    proxy = None)

        df666 = pd.DataFrame(data=fetch, index=None).reset_index(drop=False)
        return df666
    
    df1 = fetch_history(symbol)
    df1["Date"] = pd.to_datetime(df1["Date"], format = "%Y-%m-%d")
    df1["Earnings"] = df1["Date"]
    df_hist = df1
    df_er = get_er(x)
    df_merged = df_hist.merge(df_er, on = "Date", how = "left")
    df_merged.to_csv("Merged Test.csv")
    return df_merged




