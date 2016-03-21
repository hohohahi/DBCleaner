import MySQLdb
import time

ip = '10.0.10.50'
user = 'yw'
passwd = 'yuwei888k'
deleteOneOutcomeSql = "delete from Outcome_history where isLatest='N' limit 1"
sleepInteval = 1
deleteNum = 0
deleteThreshold = 1000

try:
    conn=MySQLdb.connect(host=ip,user=user,passwd=passwd,db='oddsmatrixdb',port=3306)
    cur=conn.cursor()
    while True:
        print time.strftime('%H:%M:%S',time.localtime()) + " start: " + str(deleteNum);
        cur.execute(deleteOneOutcomeSql)
        deleteNum = deleteNum + 1
        if (deleteNum > deleteThreshold):
            print("exit while circl. deleteNum:" + str(deleteNum) + "--deleteThreshold:" + str(deleteThreshold))
            break
        print time.strftime('%H:%M:%S',time.localtime()) + " end.";
        time.sleep(sleepInteval)

    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])


