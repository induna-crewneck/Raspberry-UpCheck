# Raspberry-BootNotifier v2.4 (20240105)
#	New: Let user know about reboot reason
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
import os

# define variables -------------------------------------------------------------------------------
TELEGRAM_BOT = 'telegram_bot_token'
TELEGRAM_ME  = 'target_telegram_user_id'
TELEGRAM_MSG = 'empty message'
TIMESTAMP = datetime.datetime.now()

# reading reboot-reason --------------------------------------------------------------------------
if os.path.exists('/root/Raspberry-UpCheck/RebootReason.txt'):
	with open('/root/Raspberry-UpCheck/RebootReason.txt', 'r') as file:
		RebootTimestamp = file.readline().strip() #storing first line
		RebootReason = file.readline().strip() #storing second line
	# Print the values or use them as needed
	print('RebootTimestamp: ', RebootTimestamp)
	print('RebootReason: ', RebootReason)
else:
    print('RebootReason.txt does not exist.')

# testing connection & sending update through telegram -------------------------------------------
try:
	url = 'http://ipinfo.io/json'
	try:
		response = urllib.request.urlopen(url)
	except:
		print('Error getting IP info')
	data = json.load(response)
	IP=data['ip']
	city = data['city']
	country=data['country']
	region=data['region']
	TELEGRAM_MSG='System rebooted. \nIP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP) + '\n'+ str(TIMESTAMP)
	if 'RebootTimestamp' in locals():
		TELEGRAM_MSG=TELEGRAM_MSG + '\n\nRebooted ' + RebootTimestamp + '\nReason: ' + RebootReason
	else:
		TELEGRAM_MSG=TELEGRAM_MSG + '\n\nReason unknown'
except:
	TELEGRAM_MSG='System rebooted. \nError while getting IP Info\n'+ str(TIMESTAMP)
	
url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
try:
	y = requests.post(url)
	ONLINESTATUS = 'ONLINE'
	print('DEBUG: Device is online. Telegram msg has been sent.')
except:
	ONLINESTATUS = 'OFFLINE'
	print('DEBUG: Device is offline!')

# logging ----------------------------------------------------------------------------------------
file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
file_object.write(str(TIMESTAMP) + '    SYSTEM REBOOTED & ' + ONLINESTATUS + '\n')
if 'RebootTimestamp' in locals():
	file_object.write('Reboot command sent at ' + RebootTimestamp + '\nReason: ' + RebootReason)
file_object.close()

# deleting reason txt ----------------------------------------------------------------------------
try:
    os.remove('/root/Raspberry-UpCheck/RebootReason.txt')
except Exception as e:
	print('Exception while deleting RebootReason:')
	print(e)

# Running UpChecker.py ---------------------------------------------------------------------------
exec(open('/root/Raspberry-UpCheck/UpChecker.py').read())