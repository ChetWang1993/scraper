#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import datetime
import sys
root_path = '/root/'
_root_path = '/Users/apple/Documents/trading/'
sys.path.append(root_path + 'scripts/')
from jqdatasdk import *
auth('13918125129','fmttm1993')
from utils import *
idx = '000300.XSHG'
fund_path = root_path + '/data/fund/'
fund = pd.DataFrame()
d = sys.argv[1]

stocks = get_index_stocks(idx, date = d)
#dump fund
f = get_fundamentals(query(valuation, income, indicator, finance.STK_BALANCE_SHEET).filter(valuation.code.in_(stocks)), date = d)
f['date'] = d
f.fillna(0)
f = f.rename(columns = {'code': 'ric'})
f = f.drop_duplicates()
print(fund_path + '{}.txt'.format(d))
f.to_csv(fund_path + '{}.txt'.format(d), sep='\t', index = False)