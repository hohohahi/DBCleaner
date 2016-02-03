import MySQLdb

ip = '10.0.5.220'
user = 'betbrain'
passwd = 'betbrain'

def getEventCount_FromDB_ByIdRange(start, end):
    try:
        conn=MySQLdb.connect(host=ip,user=user,passwd=passwd,db='oddsmatrixdb',port=3306)
        cur=conn.cursor()
        sql = "select e.id from OMLiveMatch_History o, Event_history e where o.oddsSource=1 and o.scoreSource=5 and o.isLatest='Y' and e.isLatest='Y' and o.eventId=e.id and e.startDate>'2016-02-03 00:00:00' and e.startDate<'2016-02-03 23:59:59'"
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

    modifiedBy = 0

    sql = "SELECT max(modifiedBy) as modifiedBy FROM TransactionEntity  WHERE eventId =" + str(eventId) + " and (multiplier=false or multiplier is null) and status in (1, 3, 4, 5) and (transactionType = 1 or transactionType=5)"
    cur.execute(sql)
    for row in cur.fetchall():
        for r in row:
            modifiedBy = r

    sql = "SELECT max(modifiedBy) as modifiedBy FROM 	TransactionMultiplier  WHERE eventId = " + str(eventId) + " and status in (1, 3, 4, 5)"
    cur.execute(sql)
    for row in cur.fetchall():
        for r in row:
            if (r>modifiedBy):
                modifiedBy = r

    cur.close()
    conn.close()
    return modifiedBy

getEventCount_FromDB_ByIdRange(0, 1)

