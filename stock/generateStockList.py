import urllib
import urllib2
import re
import os
import time

shangHaifileName = 'shangHaiStockList.txt'
shenZhenfileName = 'shenZhenStockList.txt'
splitter = '$'

def queryRealtimeData(stock):
    url = "http://hq.sinajs.cn/list=" \
          + stock;
    return httpAccess(url);

def httpAccess(url):
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res

def writeStockList(stockList, fileName):
    fp = open(fileName,'w')
    for stock in stockList:
        fp.write(str(stock)+splitter)
    fp.close()

def getFullStringForShenZhenStock(stockId):
    stockTag = ''
    if stockId <10:
       stockTag = '00000' + str(stockId)
    elif stockId>=10 and stockId<100:
        stockTag = '0000' + str(stockId)
    elif stockId>=100 and stockId<1000:
        stockTag = '000' + str(stockId)
    elif stockId>=1000 and stockId<10000:
        stockTag = '00' + str(stockId)
    elif stockId>=10000 and stockId<100000:
        stockTag = '0' + str(stockId)
    else:
        stockTag = str(stockId)

    return stockTag

def generateShangHaiStockListFile(filename):
    stockList = []
    index = 600000
    while (index < 608000):
        try:
            data = queryRealtimeData('sh' + str(index));
            dataList = data.split(',');

            if (len(dataList) > 3):
                print index
                stockList.append(index)
        except Exception,ex:
            print Exception,":",ex
            print 'Error index:' + str(index)

        index = index + 1
    writeStockList(stockList, filename)

def generateShenZhenStockListFile(filename):
    stockList = []
    index = 0
    while (index < 8000):
        try:
            stockTag = getFullStringForShenZhenStock(index)
            data = queryRealtimeData('sz' + stockTag);
            dataList = data.split(',');

            if (len(dataList) > 3):
                print index
                stockList.append(stockTag)
        except Exception,ex:
            print Exception,":",ex
            print 'Error index:' + str(index)

        index = index + 1

    index = 300000
    while (index < 301000):
        try:
            data = queryRealtimeData('sz' + str(index));
            dataList = data.split(',');

            if (len(dataList) > 3):
                print index
                stockList.append(index)
        except Exception,ex:
            print Exception,":",ex
            print 'Error index:' + str(index)

        index = index + 1

    writeStockList(stockList, filename)

generateShenZhenStockListFile(shenZhenfileName)
generateShangHaiStockListFile(shangHaifileName)