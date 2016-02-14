import smtplib
import time
from email.message import Message
from time import sleep
import email.utils
import base64

smtpserver = 'smtp.qq.com'
username = '18800761'
password = 'yuwei654321K.com'

from_addr = '18800761@qq.com'
to_addr = '18800761@qq.com'

def sendEmail():
    message = Message()
    message['Subject'] = 'Mail Subject'
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