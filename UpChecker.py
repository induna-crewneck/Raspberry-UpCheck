# Raspberry-UpCheck v2.0
# github.com/induna-crewneck/Raspberry-UpCheck/
# python

# imports ----------------------------------------------------------------------------------------
import subprocess
import requests
import os
import re
import json
from urllib2 import urlopen
import datetime

# define Variables -------------------------------------------------------------------------------
TELEGRAM_BOT = 'telegram_bot_token'
TELEGRAM_ME  = 'target_telegram_user_id'
TELEGRAM_MSG = 'empty message'
ONLINEIDENT = '0% packet loss'
TIMESTAMP = datetime.datetime.now()

# define Error handling function -----------------------------------------------------------------
def offline():
    # Logging to OnlineStatusLog.txt
    file_object = open('Raspberry-UpCheck/UpCheckerLog.txt', 'a')
    file_object.write(' \n-------------------------------------------------------------------------------------------------------- \n' + str(TIMESTAMP) + '    PING ERROR    \n' + str(error) + ' \n' + str(ping))
    file_object.close()
    
    # Rebooting system
    os.system('reboot')

def online():
    # Get IP address and IP info
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    IP=data['ip']
    city = data['city']
    country=data['country']
    region=data['region']
    
    # Sending update message via Telegram
    TELEGRAM_MSG='Pi is online (routine check) \n'+ str(TIMESTAMP) + ' \nIP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP)
    url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
    y = requests.post(url)
    # 'y' is now the reponse of sending the telegram message
    # show detailed reponse:    print y.text
    # show response code:       print y
    
    # Logging to OnlineStatusLog.txt
    file_object = open('Raspberry-UpCheck/UpCheckerLog.txt', 'a')
    file_object.write(' \n-------------------------------------------------------------------------------------------------------- \n' + str(TIMESTAMP) + '    PING SUCCESSFUL    \nIP : {3} ({2}, {0}, {1})'.format(region,country,city,IP))
    file_object.close()

# ping host url ----------------------------------------------------------------------------------
host = 'www.google.com'
ping = subprocess.Popen(
    ['ping', '-c', '4', host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)
ping, error = ping.communicate()
# 'ping' is the result of the ping command now

# search ping result for online code -------------------------------------------------------------
if ONLINEIDENT in ping: X = online()
else: X = offline()



