from jqdatasdk import *
auth('13918125129','fmttm1993')
import pandas as pd
import datetime
idx = '000300.XSHG'
from utils import *
#get trading days
dates = pd.DataFrame(data = get_trade_days(start_date = '2017-01-01', end_date = '2019-12-31'), columns = ['date'])
dates = list(dates['date'])

fund = pd.DataFrame()
for d in dates:
    print(d)
    stocks = get_index_stocks(idx, date = d)
    #dump erd
    f = get_fundamentals(query(valuation, income, indicator, finance.STK_BALANCE_SHEET).filter(valuation.code.in_(stocks)), date = d)
    f['date'] = d
    f.fillna(0)
    f = f.rename(columns = {'code': 'ric'})
    fund = fund.append(f)
fund = fund.drop_duplicates()
fund.to_csv('data/fund.txt', sep='\t', index = False)