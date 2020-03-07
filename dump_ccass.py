#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from pandas import DataFrame
import json
import os
root_path = os.path.dirname(os.path.realpath(__file__))
data_path = root_path, '/../data/scraper/ccass/'

def get_all_code(d):
    tagurl = "https://www.hkexnews.hk/sdw/search/stocklist.aspx?sortby=stockcode&shareholdingdate={}".format(d)
    response = requests.get(tagurl)
    soup = BeautifulSoup(response.text,"lxml")
    tr_list = soup.find_all("tr")
    tr_list = tr_list[2:]
    x = []
    for tr in tr_list:
        ric = tr.find('td').text.strip()
        if ric[0] == '0':
            continue
        x.append(ric)
    return x

def crawler(input_time = '2020/02/01',input_code = '00002',retry = 3):
    if retry<=0:
        return []
    try:
        timeStamp = int(time.time())
        timeArray = time.localtime(timeStamp)
        today = time.strftime("%Y%m%d", timeArray)
        headers = {
          'authority': 'www.hkexnews.hk',
          'pragma': 'no-cache',
          'cache-control': 'no-cache',
          'origin': 'https://www.hkexnews.hk',
          'upgrade-insecure-requests': '1',
          'content-type': 'application/x-www-form-urlencoded',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-user': '?1',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
          'sec-fetch-site': 'same-origin',
          'referer': 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'zh-CN,zh;q=0.9',
          'cookie': 'WT_FPC=id=119.190.82.55-367600480.30792245:lv=1580695301721:ss=1580694961314; TS016e7565=01043817a5272c3e7f85b8b507fd55d7a6ea2285e704324257e3c10df823107a8b4050228acabec6dd8a7a2a18c47e4e5dd12ab16e',
        }
        data = {
        '__EVENTTARGET': 'btnSearch',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '/wEPDwULLTIwNTMyMzMwMThkZLiCLeQCG/lBVJcNezUV/J0rsyMr',
        '__VIEWSTATEGENERATOR': 'A7B2BBE2',
        'today': today,
        'sortBy': 'shareholding',
        'sortDirection': 'desc',
        'alertMsg': 'Stock code  00000  does not exist OR not available for enquiry.',
        'txtShareholdingDate': input_time,
        'txtStockCode': input_code,
        'txtStockName': 'CLP HOLDINGS LIMITED',
        'txtParticipantID': '',
        'txtParticipantName': '',
        'txtSelPartID': ''
        }
        response = requests.post('https://www.hkexnews.hk/sdw/search/searchsdw.aspx', headers=headers, data=data)
        if response.status_code!=200:
            print("中途出错")
            return []
        soup = BeautifulSoup(response.text,"lxml")
        tr_list = soup.find_all("tr")
        tr_list = tr_list[1:]
        returndata = []
        for tr in tr_list:
            classlist = ["col-participant-id","col-participant-name","col-address","col-shareholding text-right","col-shareholding-percent text-right"]
            rowdata = []
            for cl in classlist:
                td = tr.find("td",attrs={"class":cl})
                div = td.find("div",attrs={"class":"mobile-list-body"})
                rowdata.append(div.text.strip())
            returndata.append(rowdata)
        return returndata
    except:
        print("exception")
        return crawler(input_time,input_code,retry-1)
import threading

def child_thread(input_time,total_data,code_list):
    while code_list:
        with threading.Lock():
            if code_list == []:
                code = None
            else:
                code = code_list.pop()
        if code == None:
            return
        print("正在爬取",code,"的股票信息")
        data = crawler(input_time,code)
        with threading.Lock():
            for row in data:
                total_data["时间"].append(input_time)
                total_data["股票代码"].append(code)
                total_data["Participant ID"].append(row[0])
                total_data["Name of CCASS Participant"].append(row[1])
                total_data["Address"].append(row[2])
                total_data["ShareHolding"].append(row[3])
                total_data[r"占已发行股份/认股权证/单位总数的百分比"].append(row[4])

def main():
    import sys
    if len(sys.argv) < 2:
        print("输入日期不合法")
        exit()
    d = sys.argv[1]
    input_time = d[:4]+"/"+d[4:6]+"/"+d[6:]
    print(input_time)
    total_data = {}
    col_name = ["时间","股票代码","Participant ID","Name of CCASS Participant","Address","ShareHolding",r"占已发行股份/认股权证/单位总数的百分比"]
    for cl in col_name:
        total_data[cl] = []
    codelist = get_all_code(d)
    print(codelist)
    #codelist = codelist[-500:]
    threads = []
    for i in range(40):
        t = threading.Thread(target=child_thread,args=(input_time,total_data,codelist))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    df = pd.DataFrame(total_data)
    cols = list(df)
    cols.insert(0, cols.pop(cols.index('股票代码')))
    cols.insert(1, cols.pop(cols.index('时间')))
    df.to_csv('{}/{}.csv'.format(data_path, d), index=False, sep='\t')

main()
