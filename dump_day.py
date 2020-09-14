#!/usr/local/bin/python3
#/usr/bin/python3
import pandas as pd
import datetime
import sys
import os
root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
sys.path.append(root_path + 'scripts/')
from utils import *

data_path = root_path + 'data/trading_days.txt'
d = sys.argv[1]

ret = get_trade_days(start_date = d, end_date = d)
if len(ret) == 0:
    print('china holiday {}'.format(d))
    quit()
trading_days = pd.read_csv(data_path, sep = '\t')
trading_days['date'] =  pd.to_datetime(trading_days['date'], format='%Y-%m-%d').dt.date
if 0 < trading_days[trading_days['date'] == ret[0]].size:
    quit()
trading_days = trading_days.append({'date': ret[0]}, ignore_index = True)
trading_days = trading_days.drop_duplicates()
trading_days = trading_days.sort_values(by=['date'])
trading_days.to_csv(data_path, sep = '\t', index = False)
