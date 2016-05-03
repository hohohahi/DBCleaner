import urllib
import urllib2
import re
import os
import time

fileName = 'stockList.txt'
stockList = []

def queryRealtimeData(stock):
    url = "http://hq.sinajs.cn/list=" \
          + stock;
    return httpAccess(url);

def httpAccess(url):
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res

def writeStockList():
    fp = open(fileName,'w')
    for stock in stockList:
        fp.write(str(stock)+'\n')
    fp.close()

index = 600000
while (index < 608000):
    data = queryRealtimeData('sh' + str(index));
    dataList = data.split(',');

    if (len(dataList) > 3):
        print index
        stockList.append(index)
    index = index + 1

writeStockList()

