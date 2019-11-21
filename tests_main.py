# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 

@author: Ivan Struk

"""

from earnings_parser import get_er_dates
from EOD_parser import hunt_hist
from EOD_parser import get_hist
from EOD_parser import get_hist2
import pandas as pd



def test_sample_earnings(symbol):
    stocks = symbol
    stockz = []
    re1 = []
    re2 = []
    re3 = []
    
    for i in stocks:
        try:
            print("Getting historical results for {}".format(i))
            dfw = pd.DataFrame(get_er_dates(i))
            name = i
            length_ = sum(dfw["Binary_E"])
            if length_ == 0:
                print("Skipping - No Data")
                pass
            else:
                result1 = round(((sum(dfw["PreM and Intra +"])/length_)*1),4)
                zero_denom_test = sum(dfw["Pre-Market D+"])
                if zero_denom_test == 0:
                    result2 = 0
                    continue
                else:
                    result2 = round(((sum(dfw["PreM and Intra +"])/sum(dfw["Pre-Market D+"]))*1),4)
                    result3 = round(((sum(dfw["PreM+ and Intra -"])/sum(dfw["Pre-Market D+"]))*1),4)
                stockz.append(name)
                re1.append(result1)
                re2.append(result2)
                re3.append(result3)
        except KeyError:
            print("{} is not registered in SEC EDGAR or does not exist".format(i))
            pass
        
    stock_parser = {
        "Symbol" : []    
    }
    
    results_df = pd.DataFrame(stock_parser)
    results_df["Symbol"] = stockz
    results_df["- increases in both premarket and intraday x% of the time."] = re1
    results_df["- if increasing in premarket has a x% chance of increasing in intraday."] = re2
    results_df["- if increasing in premarket has a x% change of falling in intraday."] = re3
    return results_df


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
        print(name, result)
        stock_names.append(name)
        premarket_att.append(result)
        
    stock_parser = {
        "Symbol" : [],
        "Result" : []
    }
    results_df = pd.DataFrame(stock_parser)
    results_df["Symbol"] = stock_names
    results_df["Result"] = premarket_att
    average_premarket_weight = sum(results_df["Result"])/len(results_df["Result"])
    print("On average premarket trading contributes to ",
          (round(average_premarket_weight,4)*100), 
          "% of daily price action within the selected sample.")
    print(" ")
    
    return results_df

def test_sample_indication(symbol):
    stock_names = []
    results = []
    stocks = symbol
    print("This may take a while if you have defined a large number of stocks")
    
    for i in stocks:
        df = pd.DataFrame(get_hist2(i))
        #df = df_sub.fillna(value=0)
        result = round((sum(df["H: Both True"]))/(len(list(df["H: Both True"]))),4)
        name = i
        print(name, result)
        stock_names.append(name)
        results.append(result)
        
    stock_parser = {
        "Symbol" : [],
        "Result" : []
    }
    results_df = pd.DataFrame(stock_parser)
    results_df["Symbol"] = stock_names
    results_df["Result"] = results
    final_result = sum(results_df["Result"])/len(results_df["Result"])
    print("A stock increasing or decreasing in value during premarket has a ",
          (round(final_result,4)*100), 
          "% probability of maintaining price action in the same direction.")
    return results_df


def test_sample_long(symbol):
    stocks = symbol
    stock_names = []
    results = []
    
    print("This may take a while if you have defined a large number of stocks.")
    
    for i in stocks:
        df = pd.DataFrame(hunt_hist(i))
        #df = df_sub.fillna(value=0)
        result = round((sum(df["Temp Calc1"]))/(sum(df["Pre-Market D+"])),4)
        name = i
        print(name, result)
        stock_names.append(name)
        results.append(result)
        
    stock_parser = {
        "Symbol" : [],
        "Result" : []
    }
    results_df = pd.DataFrame(stock_parser)
    results_df["Symbol"] = stock_names
    results_df["Result"] = results
    print("Result:")
    
    final_result = sum(results_df["Result"])/len(results_df["Result"])
    print("On average for the provided sample, "
          "a stock increasing in value during premarket has a ",
          (round(final_result,4)*100), 
          "% probability of further increasing in intraday.")
    
    return results_df
   

