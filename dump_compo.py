#!/usr/bin/python3
#/usr/local/bin/python3
import pandas as pd
import sys
import os
root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
sys.path.append(root_path + 'scripts/')
from utils import *
if len(sys.argv) < 2:
    print("usage: ./dump_compo.py date index")
    quit()
d = sys.argv[1]
idx = sys.argv[2]
# csi300: 000030.XSHG csi500: 000905.XSHG
compo_mapping = {'csi300': '000030.XSHG', 'csi500': '000905.XSHG'}
compo_path = root_path + 'data/compo/' + idx + '/'

if not is_bday(d):
    print('{} is holiday'.format(d))
    quit()
stocks = get_index_stocks(compo_mapping[idx], date = date_str(d))
t = get_index_weights(compo_mapping[idx], date = date_str(d))
t = t.reset_index()
t['weight'] = t['weight'] / 100
t = t.drop(columns = ['display_name', 'date'])
t = t.rename(columns={'code': 'ric'})
t = t.drop_duplicates()
t = t[['ric', 'weight']]
print(compo_path + '{}.txt'.format(d))
t.to_csv(compo_path + '{}.txt'.format(d), sep='\t', index = False)
