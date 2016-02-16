import web.parseWeb
import tool.sendEmail
from bs4 import BeautifulSoup

url = 'http://ris.szfdc.gov.cn/credit/showcjgs/esfcjgs.aspx'

def getDailyTradeNumber():
    doc =  web.parseWeb.read_page(url)
    soup = BeautifulSoup(doc, "lxml")

    #main div
    div = soup.html.body.find('div', {'id' : 'ctl00_ContentPlaceHolder1_updatepanel1'})

    #to get the date
    span = div.find('span', {'id' : 'ctl00_ContentPlaceHolder1_lblCurTime1'})
    spanText = span.text

    #to get the content
    table = div.find('table', {'id' : 'ctl00_ContentPlaceHolder1_clientList1'})
    tr = table.find('tr').next_sibling.next_sibling
    td = tr.find('td').next_sibling.next_sibling
    return spanText + ":" + td.text
#tool.sendEmail.sendEmail(spanText, td.text)




