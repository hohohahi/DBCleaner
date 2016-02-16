import urllib2

def read_page(url):
    req = urllib2.Request(url)
    con = urllib2.urlopen( req )
    doc = con.read()
    con.close()
    return doc
