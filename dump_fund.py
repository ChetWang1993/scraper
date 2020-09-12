#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import datetime
import sys
import os
root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
sys.path.append(root_path + 'scripts/')
from utils import *
fund_path = root_path + 'data/fund/'
d = sys.argv[1]

if not is_bday(d):
    print('{} is holiday'.format(d))
    quit()
stocks = get_universe(date_str(d))
f = get_fundamentals(query(valuation, income, indicator).filter(valuation.code.in_(stocks)), date = date_str(d))
f['date'] = d
f.fillna(0)
f = f.rename(columns = {'code': 'ric'})
f = f.drop_duplicates()
f = f[['date', 'ric', 'circulating_market_cap', 'inc_revenue_year_on_year', 'turnover_ratio', 'roe', 'commission_income',
    'total_operating_cost', 'operating_cost', 'capitalization']]
print(fund_path + '{}.txt'.format(d))
f.to_csv(fund_path + '{}.txt'.format(d), sep='\t', index = False)
