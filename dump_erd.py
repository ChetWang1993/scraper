#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import datetime
import sys
import os
root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../scripts/')
from utils import *
from jqdatasdk import *
auth('13918125129','fmttm1993')
idx = '000300.XSHG'
erd_path = root_path + '/../data/erd/'
d = sys.argv[1]

stocks = get_index_stocks(idx, date = date_str(d))
e = get_bars(stocks, 1, unit='1d',fields=['date','open','high','low','close','volume','money'], include_now = False,
    end_dt = next_bday_from_str(d).strftime('%Y-%m-%d'), df = True)
if 0 == e.size:
    quit()
if e['date'][0] != datetime.strptime(d, '%Y%m%d').date():
    quit()
e = e.reset_index()
e = e.drop(columns = ['level_1'])
e = e.rename(columns = {'level_0': 'ric'})
print(erd_path + '{}.txt'.format(d))
e.to_csv(erd_path + '{}.txt'.format(d), sep='\t', index = False)
