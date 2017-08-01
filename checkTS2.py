import os
import json
import tool.sendEmail

_Status_Dead_ = 5
_Status_Exception_ = 4
_Status_Error_NotContainedElement_ = 3
_Status_Parse_Error_ = 2
_Status_Parse_Warning = 1
_Status_Parse_Normal = 0

def exec_command():
    output = os.popen('curl 10.3.238.99:8888  --connect-timeout 5')
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

#exec_command()

testJson = '{"application":"webapi","service":"transport-service","status":"OK","message":"","action":""}'
rtn = parseRtnMessage(testJson)
print (rtn)
if rtn == 0:
    tool.sendEmail.sendEmail("test", "test")
#parseRtnMessage(testJson)

