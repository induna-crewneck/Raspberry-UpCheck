# Raspberry-BootNotifier v2.1 (20230429)
#	New: Action if Telegram msg fails (device is possibly offline)
# Intended as part of Raspberry-UpCheck
# 	github.com/induna-crewneck/Raspberry-UpCheck/
# This script is intended to be cronjobbed to run on every system boot. Suggested entry:
#	@reboot python3 /root/Raspberry-UpCheck/BootNotifier.py
# python3

# imports ----------------------------------------------------------------------------------------
import requests
import json
import urllib.request
import datetime

# define variables ----------------------------------------------------------------------------------------
TELEGRAM_BOT = 'telegram_bot_token'
TELEGRAM_ME  = 'target_telegram_user_id'
TELEGRAM_MSG = 'empty message'
TIMESTAMP = datetime.datetime.now()
    
# Sending update message via Telegram
TELEGRAM_MSG='System rebooted. \n'+ str(TIMESTAMP)
url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
try:
	y = requests.post(url)
	ONLINESTATUS = 'ONLINE'
	print("DEBUG: Device is online. Telegram msg has been sent.")
except:
	ONLINESTATUS = 'OFFLINE'
	print("DEBUG: Device is offline!")
# 'y' is now the reponse of sending the telegram message
# show detailed reponse:    print y.text
# show response code:       print y
    
# Logging to OnlineStatusLog.txt
file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
file_object.write(' \n-------------------------------------------------------------------------------------------------------- \n' + str(TIMESTAMP) + '    SYSTEM REBOOTED & ' + ONLINESTATUS)
file_object.close()

# Running UpChecker.py
exec(open("/root/Raspberry-UpCheck/UpChecker.py").read())
