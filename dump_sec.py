#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import datetime
import sys
import os
root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
sys.path.append(root_path + 'scripts/')
from utils import *
file_path = root_path + 'data/ind/'
d = sys.argv[1]

stocks = get_universe(date_str(d))
t = get_industry(stocks, date = date_str(d))
t = pd.DataFrame([dict(zip(['ric', 'date'] + list(t[r].keys()), [r, d] + [x['industry_code'] for x in t[r].values()])) for r in t.keys()])
if 0 == t.size:
    quit()
print(file_path + '{}.txt'.format(d))
t.to_csv(file_path + '{}.txt'.format(d), sep='\t', index = False)
