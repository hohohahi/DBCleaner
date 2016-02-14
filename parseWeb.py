import urllib2
from bs4 import BeautifulSoup
from sendEmail import *

url = 'http://ris.szfdc.gov.cn/credit/showcjgs/esfcjgs.aspx'

def read_page():
    req = urllib2.Request(url)
    con = urllib2.urlopen( req )
    doc = con.read()
    con.close()
    return doc

doc = read_page()
soup = BeautifulSoup(doc, "lxml")

#main div
div = soup.html.body.find('div', {'id' : 'ctl00_ContentPlaceHolder1_updatepanel1'})

#to get the date
span = div.find('span', {'id' : 'ctl00_ContentPlaceHolder1_lblCurTime1'})
spanText = span.text

#to get the content
content = div.find('tr', {'id' : 'TrClientList1'}).text

sendEmail(spanText, content)

