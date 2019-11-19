# Created by Ivan Struk @ Morpher

import pandas as pd


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


main_markets = qqq() + spy()
