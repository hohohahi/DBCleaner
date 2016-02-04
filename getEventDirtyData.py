import MySQLdb
import time

ip = '10.0.10.50'
user = 'yw'
passwd = 'yuwei888k'
warnThreshold = 10000
deleteThreshold = 100000
step = 10000
startId = 210000000 #210000000
endId = 217479009
sp = "sp_clear_Event_History"

#select count(*) from Event_history where id<210000000 and isLatest='N';   --0
#select max(id) from Event_history;  -- 217479009
def getEventCount_FromDB_ByIdRange(start, end, cur):
    try:
        sql = "select count(*) from Event_history where isLatest='N' and id>" + str(start) + " and id<" + str(end)
        cur.execute(sql)

        autoNum = 0
        manualNum = 0
        for row in cur.fetchall():
            for r in row:
                count = r
                if (count>warnThreshold):
                    print assembleMessage(start, end, count)

                    if (count>deleteThreshold):
                        print "call procedure " + sp + " to clean data. start:" + str(start) + "--end:" + str(end)
                        startTime = time.time()
                        cur.callproc(sp, (start, end)) #参数与存储过程有关
                        endTime = time.time()
                        print "call end. spentTime:" + str(endTime-startTime)

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def assembleMessage(startId, endId, count):
    message = str(startId) + '--' + str(endId) + '--' + str(count)
    return message

def queryEventCount_ByIdRange(startId, endId):
    if (endId < startId):
        print "startId is smaller than the endId. startId:" + str(startId) + "--endId:" + str(endId)
        return

    conn=MySQLdb.connect(host=ip,user=user,passwd=passwd,db='oddsmatrixdb',port=3306)
    cur=conn.cursor()

    if (endId - startId < step):
        print "the dif is smalll than step. run the actual value."
        getEventCount_FromDB_ByIdRange(startId, endId, cur)
    else:
        startValue = startId
        endValue = startValue + step
        while(endValue<endId):
            getEventCount_FromDB_ByIdRange(startValue, endValue, cur)
            startValue = endValue
            endValue = startValue + step

    cur.close()
    conn.close()

print "startId:" + str(startId) + "--endId:" +str(endId)
queryEventCount_ByIdRange(startId, endId)
print "over"