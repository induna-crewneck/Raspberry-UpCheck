# Raspberry-UpCheck v3.2 (20230429)
#	New: a few more failsaves if connections fail
#
# 	github.com/induna-crewneck/Raspberry-UpCheck/
# This is intended to check internet connection and VPN connection integrity,
#	notify the user (telegram) about the status and take action (reboot) on a fail.
# This script can be cronjobbed to run every few hours or every day. Suggested entry:
#	0 */3 * * * sudo python3 /root/Raspberry-UpCheck/UpChecker.py
# python3

# imports ----------------------------------------------------------------------------------------
import subprocess
import requests
import os
import re
import json
import urllib.request
import datetime

# define Variables -------------------------------------------------------------------------------
TELEGRAM_BOT = 'telegram_bot_token'
TELEGRAM_ME  = 'target_telegram_user_id'
TELEGRAM_MSG = 'empty message'
ONLINEIDENT = '0% packet loss'
TIMESTAMP = datetime.datetime.now()
BADCOUNTRY = 'badcountrycode'

# define Error handling function -----------------------------------------------------------------
def offline():
    # Logging to OnlineStatusLog.txt
    file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
    file_object.write(' \n-------------------------------------------------------------------------------------------------------- \n' + str(TIMESTAMP) + '    PING ERROR    \n' + str(error) + ' \n' + str(ping))
    file_object.close()
    # Rebooting system
    os.system('reboot')

def online():
    # Get IP address and IP info
    url = 'http://ipinfo.io/json'
    response = urllib.request.urlopen(url)
    data = json.load(response)
    IP=data['ip']
    city = data['city']
    country=data['country']
    region=data['region']

    # Checking country
    if country == BADCOUNTRY:
      file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
      file_object.write(' \n-------------------------------------------------------------------------------------------------------- \n' + str(TIMESTAMP) + '    COUNTRY MEETS REBOOT CRITERIA    \nIP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP))
      file_object.close()
      TELEGRAM_MSG='WARNING!\nILLEGAL COUNTRY DETECTED!\n'+ str(TIMESTAMP) + ' \nIP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP) + ' \nWill attempt reboot now.'
      url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
      try:
      	y = requests.post(url)
      except:
      	X = offline()
      # Rebooting system
      os.system('reboot')

    # Sending update message via Telegram
    TELEGRAM_MSG='Pi is online (routine check) \n'+ str(TIMESTAMP) + ' \nIP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP)
    url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
    try:
    	y = requests.post(url)
    except:
    	X = offline()
    # 'y' is now the reponse of sending the telegram message
    # show detailed reponse:    print y.text
    # show response code:       print y
    
    # Logging to OnlineStatusLog.txt
    file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
    file_object.write(' \n-------------------------------------------------------------------------------------------------------- \n' + str(TIMESTAMP) + '    PING SUCCESSFUL    \nIP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP))
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

if ONLINEIDENT in str(ping):
	try:
		X = online()
	except:
		os.system('reboot')
else: X = offline()
