from jqdatasdk import *
auth('13918125129','fmttm1993')
import pandas as pd
import datetime
idx = '000300.XSHG'
from utils import *
#get trading days
dates = pd.DataFrame(data = get_trade_days(start_date = '2017-01-01', end_date = '2019-12-31'), columns = ['date'])
#dates.to_csv('trading_days.txt', index = False, sep='\t')
dates = list(dates['date'])

erd = pd.DataFrame()
for d in dates:
    print(d)
    stocks = get_index_stocks(idx, date = d)
    #dump erd
    e = get_bars(stocks, 8, unit='30m',fields=['date','open','high','low','close','volume','money'], include_now=False,end_dt=get_day_offset(d, 1), df = True)
    e = e[e['date'].dt.time == datetime.time(10,30)]    
    e = e.reset_index()
    e = e.drop(columns = ['level_1'])
    e = e.rename(columns = {'level_0': 'ric'})
    e['date'] = e['date'].dt.date()
    erd = erd.append(e)
erd = erd.drop_duplicates()
erd.to_csv('data/ten.txt', sep='\t', index = False)