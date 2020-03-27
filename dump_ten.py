#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import datetime
root_path = '/root/'
_root_path = '/Users/apple/Documents/trading/'
sys.path.append(root_path + 'scripts/')
from utils import *
from jqdatasdk import *
auth('13918125129','fmttm1993')
idx = '000300.XSHG'
ten_path = root_path + '/data/ten/'
d = sys.argv[1]

stocks = get_index_stocks(idx, date = d)
#dump erd
e = get_bars(stocks, 8, unit='30m',fields=['date','open','high','low','close','volume','money'], include_now=False,
    end_dt = next_bday_from_str(d).strftime('%Y-%m-%d'), df = True)
e = e[e['date'].dt.time == datetime.time(10,30)]
if 0 == e.size:
    quit()
if e['date'][0] != datetime.strptime(d, '%Y%m%d').date():
    quit()
e = e.reset_index()
e = e.drop(columns = ['level_1'])
e = e.rename(columns = {'level_0': 'ric'})
print(ten_path + '{}.txt'.format(d))

erd.to_csv(ten_path + '{}.txt'.format(d), sep='\t', index = False)
