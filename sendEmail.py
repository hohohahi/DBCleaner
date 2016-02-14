import smtplib
import time
from email.message import Message
from time import sleep
from email.mime.text import MIMEText
import email.utils
import base64
from email.header import Header

smtpserver = 'smtp.qq.com'
username = '18800761'
password = 'yuwei654321K.com'

from_addr = '18800761@qq.com'
to_addr = '18800761@qq.com'

def sendEmail(subject, content):
    message = MIMEText(content.encode('utf-8'), 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = from_addr
    message['To'] = to_addr
    msg = message.as_string()

    sm = smtplib.SMTP(smtpserver,port=587,timeout=20)
    sm.set_debuglevel(1)
    sm.starttls()
    sm.login(username, password)

    sm.sendmail(from_addr, to_addr, msg)
    sleep(5)
    sm.quit()