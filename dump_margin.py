import tushare as ts
from utils import *
from jqdatasdk import *
auth('13918125129','fmttm1993')
import pandas as pd
import datetime
from pathlib import Path

pro = ts.pro_api()
ts.set_token('bf143268f4dc8b4c8f4b8656486f6a090403bd7a332ea60220a7c017')
df = pro.margin_detail(trade_date='20180802')
idx = '000300.XSHG'
dates = pd.DataFrame(data = get_trade_days(start_date = '2019-01-01', end_date = '2019-12-31'), columns = ['date'])
dates = list(dates['date'])
margin = pd.read_csv('data/margin.txt', sep = '\t') if Path('data/margin.txt').exists() else pd.DataFrame()

def ric_mapping(x):
    y = x.split('.'); return y[0] + ('.XSHG' if y[1] == 'SH' else '.XSHE')
for d in dates:
    print(d)
    t = pro.margin_detail(trade_date = d.strftime('%Y%m%d'))
    t['ts_code'] = t['ts_code'].apply(ric_mapping)
    t = t.rename(columns = {'ts_code': 'ric'})
    margin = margin.append(t)

margin = margin.drop_duplicates()
margin.to_csv('data/margin.txt', sep='\t', index = False)