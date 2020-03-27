#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import datetime
import sys
import os
root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
sys.path.append(root_path + 'scripts/')
from utils import *
bar_path = root_path + 'data/bar/'
d = sys.argv[1]
data_path = root_path + 'data/trading_days.txt'
trading_days = pd.read_csv(data_path, sep = '\t')
if 0 == trading_days[trading_days['date'] == date_str(d)].size:
    print('{} is holiday'.format(d))
    quit()
from jqdatasdk import *
auth('13918125129','fmttm1993')
idx = '000300.XSHG'
stocks = get_index_stocks(idx, date = date_str(d))
e = get_bars(stocks, 48, unit='5m',fields=['date','open','high','low','close','volume','money'], include_now = False,
    end_dt = next_bday_from_str(d).strftime('%Y-%m-%d'), df = True)
if 0 == e.size:
    quit()
if e['date'][0].date() != datetime.strptime(d, '%Y%m%d').date():
    quit()
e = e.reset_index()
e = e.drop(columns = ['level_1'])
e = e.rename(columns = {'level_0': 'ric'})
print(bar_path + '{}.txt'.format(d))
e.to_csv(bar_path + '{}.txt'.format(d), sep='\t', index = False)
