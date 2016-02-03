import MySQLdb

ip = '10.0.5.220'
user = 'betbrain'
passwd = 'betbrain'

def getEventCount_FromDB_ByIdRange(start, end):
    try:
        conn=MySQLdb.connect(host=ip,user=user,passwd=passwd,db='oddsmatrixdb',port=3306)
        cur=conn.cursor()
        sql = "select id from Event_history where isLatest='N' and id>" + str(start) + " and id<" + str(end) + " limit 1"
        cur.execute(sql)

        autoNum = 0
        manualNum = 0
        for row in cur.fetchall():
            for r in row:
                eventId = r
                modifiedBy = getMaxModifiedBy_ByEventId(eventId)
                if (modifiedBy>0):
                    manualNum = manualNum + 1
                else:
                    autoNum = autoNum + 1

        print "autoNum:" + str(autoNum)
        print "manualNum:" + str(manualNum)

        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def getMaxModifiedBy_ByEventId(eventId):
    conn=MySQLdb.connect(host=ip,user=user,passwd=passwd,db='oddsmatrixdb',port=3306)
    cur=conn.cursor()
    sql = "SELECT max(modifiedBy) as modifiedBy FROM TransactionEntity  WHERE eventId =" + str(eventId) + " and (multiplier=false or multiplier is null) and status in (1, 3, 4, 5) and (transactionType = 1 or transactionType=5)"
    cur.execute(sql)

    modifiedBy = 0
    for row in cur.fetchall():
        for r in row:
            modifiedBy = r

    cur.close()
    conn.close()
    return modifiedBy

getMaxModifiedBy_ByEventId(22833794)

