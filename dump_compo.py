from jqdatasdk import *
auth('13918125129','fmttm1993')
import pandas as pd
import datetime
idx = '000300.XSHG'
#get trading days
dates = pd.DataFrame(data = get_trade_days(start_date = '2017-01-01', end_date = '2019-12-31'), columns = ['date'])
dates = list(dates['date'])

weights = pd.DataFrame()
for d in dates:
    print(d)
    stocks = get_index_stocks(idx, date = d)
    w = get_index_weights(idx, date = d.strftime('%Y-%m-%d'))
    w = w.reset_index()
    w['weight'] = w['weight'] / 100
    weights = weights.append(w.drop(columns = ['display_name']))
weights = weights.drop_duplicates()
weights.to_csv('weights.txt', sep='\t', index = False)