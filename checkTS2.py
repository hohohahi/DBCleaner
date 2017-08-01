import os
import json
import tool.sendEmail
import sched
import time
import threading

_Status_Dead_ = 5
_Status_Exception_ = 4
_Status_Error_NotContainedElement_ = 3
_Status_Parse_Error_ = 2
_Status_Parse_Warning = 1
_Status_Parse_Normal = 0

devIP = "10.3.238.20"
stageIP = "10.3.238.21"
prod_env1_IPs = ["10.3.240.14", "10.3.240.11", "10.3.240.13", "10.3.240.12"]
prod_env3_IPs = ["10.3.239.11", "10.3.239.14", "10.3.239.12", "10.3.239.13"]

def exec_command_ByIP(ip):
    command = 'curl '+ ip + ':8888  --connect-timeout 5'
    output = os.popen(command)
    print (output.read())

def parseRtnMessage(message):
    rtnStatus = _Status_Parse_Normal;
    try:
        jsonMessage = json.loads(message)
        statusValue = jsonMessage['status']
        if statusValue is None:
            print ("error")
        else:
            if (statusValue == 'OK'):
                statusValue = _Status_Parse_Normal
            elif (statusValue == 'WARNING'):
                statusValue = _Status_Parse_Warning
            elif (statusValue == 'CRITICAL'):
                statusValue = _Status_Parse_Error_
    except Exception:
        statusValue = _Status_Exception_

    return statusValue

def checkByIP(ip, tag):
    rtnMessage = exec_command_ByIP(ip)
    rtnCode = parseRtnMessage(rtnMessage)
    if (_Status_Parse_Normal != rtnCode):
        title = tag + " " + ip + " Alert!!!"
        body = "Code:" + str(rtnCode) + ", message:" + rtnMessage
        tool.sendEmail.sendEmail(title, body)
    else:
        title = tag + " " + ip + " Good"
        body = "..."
        tool.sendEmail.sendEmail(title, body)

def check():
    checkByIP(devIP, 'dev');
    checkByIP(stageIP, 'stage');

    checkByIP(prod_env1_IPs[0], 'Prod Env1 1');
    checkByIP(prod_env1_IPs[1], 'Prod Env1 2');
    checkByIP(prod_env1_IPs[2], 'Prod Env1 3');
    checkByIP(prod_env1_IPs[3], 'Prod Env1 4');

    checkByIP(prod_env3_IPs[0], 'Prod Env3 1');
    checkByIP(prod_env3_IPs[1], 'Prod Env3 2');
    checkByIP(prod_env3_IPs[2], 'Prod Env3 3');
    checkByIP(prod_env3_IPs[3], 'Prod Env3 4');
    
timer = threading.Timer(60, check)
timer.start()

#checkByIP(devIP, 'dev');
#exec_command()

#testJson = '{"application":"webapi","service":"transport-service","status":"OK","message":"","action":""}'
#rtn = parseRtnMessage(testJson)
#print (rtn)
#if rtn == 0:
#    tool.sendEmail.sendEmail("test", "test")
#parseRtnMessage(testJson)
