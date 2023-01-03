# Raspberry-BootNotifier v2
# Intended as part of Raspberry-UpCheck
# github.com/induna-crewneck/Raspberry-UpCheck/
# python

# imports ----------------------------------------------------------------------------------------
import requests
import json
import urllib.request
import datetime

# define Variables -------------------------------------------------------------------------------
TELEGRAM_BOT = '5218238124:AAFWAZHVWLP41pYiaEno7kDYJfM0beIxkv0'
TELEGRAM_ME  = '827869116'
TELEGRAM_MSG = 'empty message'
TIMESTAMP = datetime.datetime.now()
    
# Sending update message via Telegram
TELEGRAM_MSG='System rebooted. \n'+ str(TIMESTAMP)
url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
y = requests.post(url)
# 'y' is now the reponse of sending the telegram message
# show detailed reponse:    print y.text
# show response code:       print y
    
# Logging to OnlineStatusLog.txt
file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
file_object.write(' \n-------------------------------------------------------------------------------------------------------- \n' + str(TIMESTAMP) + '    SYSTEM REBOOTED')
file_object.close()

# Running UpChecker.py
exec(open("/root/Raspberry-UpCheck/UpChecker.py").read())
