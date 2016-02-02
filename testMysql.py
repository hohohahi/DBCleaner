import MySQLdb

try:
    conn=MySQLdb.connect(host='109.205.92.50',user='om',passwd='bestbrainer',db='oddsmatrixdb',port=3306)
    cur=conn.cursor()
    cur.execute('select count(*) from Location_history')
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1]) 