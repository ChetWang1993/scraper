#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import datetime
import sys
import os
root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
sys.path.append(root_path + 'scripts/')
from utils import *

if len(sys.argv) < 3:
    print("usage: ./dump_erd.py date index")
    quit()
d = sys.argv[1]
idx = sys.argv[2]
if not is_bday(d):
    print('{} is holiday'.format(d))
    quit()
if idx == 'a50':
    stocks = ['000016.XSHG']
    erd_path = root_path + 'data/erd/a50/'
else:
    stocks = get_universe(date_str(d))
    erd_path = root_path + 'data/erd/cn/'
e = get_bars(stocks, 1, unit='1d',fields=['date','open','high','low','close','volume','money'], include_now = False,
    end_dt = next_bday_from_str(d).strftime('%Y-%m-%d'), df = True, fq_ref_date = date.today())
if 0 == e.size:
    quit()
e = e[e['date'] == datetime.strptime(d, '%Y%m%d').date()]
if e['date'][0] != datetime.strptime(d, '%Y%m%d').date():
    quit()
e = e.reset_index()
e = e.drop(columns = ['level_1'])
e = e.rename(columns = {'level_0': 'ric'})
print(erd_path + '{}.txt'.format(d))
e.to_csv(erd_path + '{}.txt'.format(d), sep='\t', index = False)
