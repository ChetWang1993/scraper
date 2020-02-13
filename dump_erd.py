#!/usr/bin/python3
import pandas as pd
import datetime
import sys
root_path= '/root/'
sys.path.append(root_path + 'scripts/')
from utils import *
from jqdatasdk import *
auth('13918125129','fmttm1993')

def date_str(d):
    return d[:4] + '-' + d[4:6] + '-' + d[6:]
idx = '000300.XSHG'
erd_path = root_path + '/data/prod/erd/'
_erd_path = '/Users/apple/Documents/trading/alpha/data/erd/'
d = sys.argv[1]

stocks = get_index_stocks(idx, date = date_str(d))
e = get_bars(stocks, 1, unit='1d',fields=['date','open','high','low','close','volume','money'], include_now = False,
    end_dt = next_bday_from_str(d).strftime('%Y-%m-%d'), df = True)
if 0 == e.size:
    quit()
print(e['date'][0])
if e['date'][0] != datetime.strptime(d, '%Y%m%d').date():
    quit()
e = e.reset_index()
e = e.drop(columns = ['level_1'])
e = e.rename(columns = {'level_0': 'ric'})
print(erd_path + '{}.txt'.format(d))
e.to_csv(erd_path + '{}.txt'.format(d), sep='\t', index = False)
