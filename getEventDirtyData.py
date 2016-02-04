import MySQLdb

ip = '10.0.10.50'
user = 'yw'
passwd = 'yuwei888k'
threshold = 10000
step = 10000
startId = 217409009 #210000000
endId = 217479009

#select count(*) from Event_history where id<210000000 and isLatest='N';   --0
#select max(id) from Event_history;  -- 217479009
def getEventCount_FromDB_ByIdRange(start, end):
    try:
        conn=MySQLdb.connect(host=ip,user=user,passwd=passwd,db='oddsmatrixdb',port=3306)
        cur=conn.cursor()
        sql = "select count(*) from Event_history where isLatest='N' and id>" + str(start) + " and id<" + str(end)
        cur.execute(sql)

        autoNum = 0
        manualNum = 0
        for row in cur.fetchall():
            for r in row:
                count = r
                if (count>threshold):
                    print assembleMessage(start, end, count)

        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def assembleMessage(startId, endId, count):
    message = str(startId) + '--' + str(endId) + '--' + count

def queryEventCount_ByIdRange(startId, endId):
    if (startId < endId):
        print "startId is smaller than the endId. startId:" + str(startId) + "--endId:" + str(endId)
        return

    if (startId - endId < step):
        print "the dif is smalll than step. run the actual value."
        getEventCount_FromDB_ByIdRange(startId, endId)
    else:
        startValue = startId
        endValue = startValue + step
        while(endValue<endId):
            getEventCount_FromDB_ByIdRange(startValue, endValue)
            startValue = endValue
            endValue = startValue + step

print "startId:" + str(startId) + "--endId:" +str(endId)
queryEventCount_ByIdRange(startId, endId)
print "over"