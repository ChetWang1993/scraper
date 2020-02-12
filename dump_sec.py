from jqdatasdk import *
auth('13918125129','fmttm1993')
import pandas as pd
import datetime
from utils import *
idx = '000300.XSHG'
#get trading days
dates = pd.DataFrame(data = get_trade_days(start_date = '2017-01-01', end_date = '2019-12-31'), columns = ['date'])
dates = list(dates['date'])
ind = pd.DataFrame()
for d in dates:
    print(d)
    stocks = get_index_stocks(idx, date = d)
    i = get_industry(stocks, date = d)
    t = pd.DataFrame([dict(zip(['ric', 'date'] + list(i[r].keys()), [r, d] + [x['industry_code'] for x in i[r].values()])) for r in i.keys()])
    ind = ind.append(t)
ind = ind.drop_duplicates()
ind.to_csv('ind.txt', sep='\t', index = False)