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


def getDateList(ticker):
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?type=10-&dateb=&owner=include&count=100&action=getcompany&CIK=%s' % ticker
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
            #converted = datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%m/%d/%Y')
            converted = datetime.datetime.strptime(date,"%Y-%m-%d").strftime("%Y-%m-%d")
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
    #df_merged.to_csv("Merged Test.csv")
    return df_merged

def get_er_dates(symbol):
        dfq = give_df(symbol)
        dfq["Binary_E"] = np.where(dfq['Event'] == "Earnings", 1, 0)
        #dfq["Binary_-1"] = np.where(dfq["Binary_E"].shift(-1) == 1, 1, 0)
        dfq["Pre-Market Change"] = dfq["Open"] - dfq["Close"].shift(+1)
        dfq["Intraday Change"] = dfq["Close"] - dfq["Open"]
        dfq["Pre-Market D+"] = np.where(dfq['Pre-Market Change']>0, 1, 0)
        dfq["Intraday D+"] = np.where(dfq['Intraday Change']>0, 1, 0)
        dfq["Pre-Market D-"] = np.where(dfq['Pre-Market Change']<0, 1, 0)
        dfq["Intraday D-"] = np.where(dfq['Intraday Change']<0, 1, 0)
        dfq["PreM and Intra +"] = np.where(dfq['Pre-Market D+'] +
                                           dfq["Intraday D+"] > 1, 1, 0)
        dfq["PreM+ and Intra -"] = np.where(dfq['Pre-Market D+'] +
                                           dfq["Intraday D-"] > 1, 1, 0)
        dfw = dfq.dropna()
        return dfw
