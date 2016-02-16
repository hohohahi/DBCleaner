import web.parseWeb
import tool.sendEmail
from bs4 import BeautifulSoup

url = 'http://shenzhen.anjuke.com/community/view/97440'

def getDailyPrice():
    doc =  web.parseWeb.read_page(url)
    soup = BeautifulSoup(doc, "lxml")

    div = soup.html.body.find('em', {'class' : 'comm-avg-price'})
    return div.text


