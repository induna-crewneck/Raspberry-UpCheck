# python

# imports ----------------------------------------------------------
import subprocess
import requests
import os
import re
import json
from urllib2 import urlopen

# define Variables -------------------------------------------------
TELEGRAM_BOT = 'telegram_bot_token'
TELEGRAM_ME  = 'target_telegram_user_id'
TELEGRAM_MSG = 'messagecontent'
OFFLINEIDENT = '100% packet loss'

# ping host url ----------------------------------------------------
host = 'www.google.com'
ping = subprocess.Popen(
    ['ping', '-c', '4', host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)
ping, error = ping.communicate()
# 'ping' is the result of the ping command now

# Get IP address ---------------------------------------------------
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
IP=data['ip']
city = data['city']
country=data['country']
region=data['region']

# search ping result for offline code ------------------------------
if OFFLINEIDENT in ping: TELEGRAM_MSG='ping timed out'
else: TELEGRAM_MSG='Pi is online  \nIP : {3} \nRegion : {0} \nCountry : {1} \nCity : {2}'.format(region,country,city,IP)

# send results to telegram -----------------------------------------
url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
x = requests.post(url)
# 'x' is now the reponse of sending the telegram message
# show detailed reponse:    print x.text
# show response code:       print x
