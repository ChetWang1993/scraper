#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import datetime
import sys
root_path = '/root/'
_root_path = '/Users/apple/Documents/trading/'
sys.path.append(root_path, 'scripts/')
from utils import *
from jqdatasdk import *
auth('13918125129','fmttm1993')
from utils import *
idx = '000300.XSHG'
compo_path = root_path, '/data/compo/'
d = sys.argv[1]

stocks = get_index_stocks(idx, date = date_str(d))
w = get_index_weights(idx, date = date_str(d))
w = w.reset_index()
w['weight'] = w['weight'] / 100
w = w.drop(columns = ['display_name', 'date'])
w = w.rename(columns={'code': 'ric'})
w = w.drop_duplicates()
print(compo_path + '{}.txt'.format(d))
w.to_csv(compo_path + '{}.txt'.format(d), sep='\t', index = False)
