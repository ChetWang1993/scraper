#!/usr/bin/python3
#/usr/local/bin/python3
import sys
import pandas as pd
from jqdatasdk import *
auth('13918125129','fmttm1993')
_data_path = '/root/data/prod/trading_days.txt'
data_path = '/Users/apple/Documents/trading/alpha/data/trading_days.txt'
d = sys.argv[1]
_d = '20200210'

ret = get_trade_days(start_date = d, end_date = d)
if len(ret) == 0:
    quit()
trading_days = pd.read_csv(data_path, sep = '\t')
trading_days['date'] =  pd.to_datetime(trading_days['date'], format='%Y-%m-%d').dt.date
if 0 < trading_days[trading_days['date'] == ret[0]].size:
    quit()
trading_days = trading_days.append({'date': ret[0]}, ignore_index = True)
trading_days = trading_days.drop_duplicates()
trading_days.to_csv(data_path, sep = '\t')
