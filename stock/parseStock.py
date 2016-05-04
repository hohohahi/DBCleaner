import urllib
import urllib2
import time
import datetime
import web.parseWeb
import tool.sendEmail
from bs4 import BeautifulSoup
import re
import os
import time

countedDay = 10
shangHaifileName = 'shangHaiStockList.txt'
shenZhenfileName = 'shenZhenStockList.txt'
splitter = '$'

def queryHistoryData(fromYear, fromMonth, fromDay, toYear, toMonth, toDay, stock):
    url = "http://ichart.yahoo.com/table.csv?s=" \
          + stock \
          + "&a=" + str(fromMonth) + "&b=" + str(fromDay) + "&c=" + str(fromYear) \
          + "&d=" + str(toMonth) + "&e=" + str(toDay) + "&f=" + str(toYear) \
          + "&g=d"
    return httpAccess(url)

def queryRealtimeData(stock):
    url = "http://hq.sinajs.cn/list=" \
          + stock;
    return httpAccess(url);

def httpAccess(url):
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res

def calculate(high, low, open, close, volume):
    high_int = float(high);
    low_int = float(low);
    open_int = float(open);
    close_int = float(close);
    volume_int = int(volume)/100;

    var1 = close_int - low_int;
    var2 = high_int - low_int;
    var3 = close_int - high_int;

    var4 = 0;

    if (high_int > low_int):
        var4 = (var1/var2 + var3/var2)*volume_int;
    else:
        var4 = 0;

    return var4;

def getHistoryData(countedDay, stockTag):
    currentTime = time.mktime(time.gmtime()) + 3600*8
    toTime = currentTime - 24*60*60
    toTimeStruct = time.localtime(toTime)
    toTimeYear = time.strftime('%Y',toTimeStruct)
    toTimeMonth = time.strftime('%m',toTimeStruct)
    toTimeDay = time.strftime('%d',toTimeStruct)

    fromTime = currentTime - 20*24*60*60
    fromTimeStruct = time.localtime(fromTime)
    fromTimeYear = time.strftime('%Y',fromTimeStruct)
    fromTimeMonth = time.strftime('%m',fromTimeStruct)
    fromTimeDay = time.strftime('%d',fromTimeStruct)

    historyData = queryHistoryData(fromTimeYear, str(int(fromTimeMonth)-1), fromTimeDay, toTimeYear, str(int(toTimeMonth)-1), toTimeDay, stockTag);
    list = historyData.split('\n')

    validNum = 0
    totalValue = 0
    for element in list:
        lineDetails = element.split(',')
        if (lineDetails[0] == 'Date'):
            continue

        if (len(lineDetails) == 7):
            open = lineDetails[1]
            high = lineDetails[2]
            low = lineDetails[3]
            close = lineDetails[4]
            volume = lineDetails[5]
            volume_int = int(volume)
            if (validNum <countedDay):
                value = calculate(high, low, open, close, volume);
                totalValue = totalValue + value
                validNum = validNum + 1
    return totalValue

def getRealData(stockTagForReal):
    data = queryRealtimeData(stockTagForReal);
    dataList = data.split(',');

    if (len(dataList) < 3):
        print 'Warning: missing realtime details, stockId:' + str(stockId)
        return 0;

    open =  dataList[1]
    current = dataList[3]
    high = dataList[4]
    low = dataList[5]
    volume = dataList[8]
    currentValue = calculate(high, low,open, current, volume)

    return currentValue

def loadStockList(filename):
    fp = open(filename,'r')
    try:
        all_the_text = fp.read()
        stockList = all_the_text.split(splitter)
    finally:
        fp.close( )

    return stockList

def getStockTagForShangHaiHistory(stockId):
    stockTag = stockId + '.SS'
    return stockTag

def getStockTagForShangHaiReal(stockId):
    stockTag = 'sh' + stockId
    return stockTag

def getStockTagForShenZhenReal(stockId):
    stockTag = 'sz' + stockId
    return stockTag

def getStockTagForShenZhenHistory(stockId):
    stockTag = stockId + '.SZ'
    return stockTag

def checkShangHaiIndex(stockList):
    for stock in stockList:
        try:
            stockTagForReal = getStockTagForShangHaiReal(stock)
            realValue = getRealData(stockTagForReal);

            if (realValue == 0):
                continue

            stockTagForHistory = getStockTagForShangHaiHistory(stock)
            historyValue = getHistoryData(countedDay, stockTagForHistory);
            finalValue = (float(realValue) + float(historyValue))/10000;

            if (finalValue > 5):
                print 'stock:' + str(stock) + '--CYW:' + str(finalValue);
        except Exception,ex:
            print Exception,":",ex
            print 'Error index:' + str(stock)

def checkShenZhenIndex(stockList):
    for stock in stockList:
        print stock
        try:
            stockTagForReal = getStockTagForShenZhenReal(stock)
            realValue = getRealData(stockTagForReal);

            if (realValue == 0):
                continue

            stockTagForHistory = getStockTagForShenZhenHistory(stock)
            historyValue = getHistoryData(countedDay, stockTagForHistory);
            finalValue = (float(realValue) + float(historyValue))/10000;

            if (finalValue > 5):
                print 'stock:' + str(stock) + '--CYW:' + str(finalValue);
        except Exception,ex:
            print Exception,":",ex
            print 'Error index:' + str(stock)

stockList = loadStockList(shangHaifileName)
checkShangHaiIndex(stockList)
#stockList = loadStockList(shenZhenfileName)
#checkShenZhenIndex(stockList)