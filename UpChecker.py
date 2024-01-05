# Raspberry-UpCheck v4.1 (20240105)
#	New: Let user know about reboot reason
#
# 	github.com/induna-crewneck/Raspberry-UpCheck/
# This is intended to check internet connection and VPN connection integrity,
#	notify the user (telegram) about the status and take action (reboot) on a fail.
# This script can be cronjobbed to run every few hours or every day. Suggested entry:
#	0 */3 * * * sudo python3 /root/Raspberry-UpCheck/UpChecker.py
# python3

DEBUG = 0		# enable DEBUG printing with "1", disable with "0"

# imports ----------------------------------------------------------------------------------------
import subprocess
import requests
import os
import re
import json
import urllib.request
import datetime
import time

# define Variables -------------------------------------------------------------------------------
TELEGRAM_BOT = 'telegram_bot_token'
TELEGRAM_ME  = 'target_telegram_user_id'
TELEGRAM_MSG = 'empty message'
ONLINEIDENT = '0% packet loss'
OFFLINEIDENT = 'Temporary failure in name resolution'
TIMESTAMP = datetime.datetime.now()
BADCOUNTRY = 'badcountrycode'

# define Error handling function -----------------------------------------------------------------
def testmsg():
	if DEBUG == 1: print('		  DEBUG: testmsg() triggered')
	TELEGRAM_MSG='Test Message\n'+ str(TIMESTAMP)
	telegramurl = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
	try:
		y = requests.post(telegramurl)
	except Exception as e:
		if DEBUG == 1: print(f'		  DEBUG: Error while sending Telegram message (test): {e}')
		offline()

def offline(reason):
	if DEBUG == 1: print('			   DEBUG: offline() triggered')
	# Logging to OnlineStatusLog.txt
	file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
	file_object.write(str(TIMESTAMP) + '	PING ERROR:	' + str(error) + ' \n			   ' + str(ping) + '\n')
	file_object.close()
	# Writing reboot reason
	file_object = open('/root/Raspberry-UpCheck/RebootReason.txt', 'a')
	file_object.write(str(TIMESTAMP) + '\n' + reason)
	file_object.close()
	# Rebooting
	os.system('reboot')

def online():
	# Get IP address and IP info
	url = 'http://ipinfo.io/json'
	try:
		if DEBUG == 1: print('			   DEBUG: Getting IP info')
		response = urllib.request.urlopen(url)
	except Exception as e:
		print(f'				DEBUG: Exception while getting IP info: {e}')
		# if DEBUG == 1: X = testmsg()
		reason = 'Exception while checking IP. Device likely offline.'
		offline(reason)
		return
	data = json.load(response)
	IP=data['ip']
	city = data['city']
	country=data['country']
	region=data['region']

	# Checking country
	if country == BADCOUNTRY:
		os.system('systemctl stop qbittorrent')
		print(str(TIMESTAMP)+' Bad country detected')
		file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
		file_object.write(str(TIMESTAMP) + '	BAD COUNTRY (1)		IP : {3} ({2}, {0}, {1})\n'.format(region,country,city,IP))
		file_object.close()
		TELEGRAM_MSG='WARNING!\nIP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP) + ' \nRestarting OpenVPN\n'+ str(TIMESTAMP)
		telegramurl = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
		try:
			y = requests.post(telegramurl)
		except Exception as e:
			if DEBUG == 1: print(f'			   DEBUG: Error while sending Telegram message (1): {e}')
			reason = 'Exception while restarting OpenvVPN after IP rule exception. Device likely offline.'
			offline(reason)
			return
		# Restarting OpenVPN
		os.system('systemctl restart openvpn')
		time.sleep(10)
		print('			   OpenVPMN restarted')
		#checking country again
		print('			   DEBUG: Getting IP info (2)')
		try:
			response = urllib.request.urlopen(url)
		except Exception as e:
			print(f'				DEBUG: Error while getting IP info (2): {e}')
		reason = 'Exception while checking IP after restarting OpenVPN. Device likely offline.'
		offline(reason)
		data = json.load(response)
		IP=data['ip']
		city = data['city']
		country=data['country']
		region=data['region']
		if country == BADCOUNTRY:
			print('			   Still bad: '+country)
			file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
			file_object.write(str(TIMESTAMP) + '	BAD COUNTRY (2)		IP : {3} ({2}, {0}, {1})\n'.format(region,country,city,IP))
			file_object.close()
			TELEGRAM_MSG='Issue not reolved!\nRebooting now'
			telegramurl = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
			try:
				y = requests.post(telegramurl)
			except Exception as e:
				if DEBUG == 1: print(f'			   DEBUG: Error while sending Telegram message (2): {e}')
				reason = 'Exception while notifying user about IP rule exception after OpenVPN restart. Device likely offline.'
				offline(reason)
				return
		else:
			os.system("systemctl restart qbittorrent sonarr radarr")
			print('			   Issue resolved')
			TELEGRAM_MSG='Issue resolved\nNew IP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP)
			url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
			try:
				y = requests.post(url)
			except Exception as e:
				if DEBUG == 1: print(f'			   DEBUG: Error while sending Telegram message (3): {e}')
				reason = 'Exception while notifying user about resolved IP rule exception. Device likely offline.'
				offline(reason)
				return
	else:
		print(str(TIMESTAMP)+' All good. {3} ({2}, {0}, {1})'.format(region,country,city,IP))
	
	# Logging to OnlineStatusLog.txt
	file_object = open('/root/Raspberry-UpCheck/UpCheckerLog.txt', 'a')
	file_object.write(str(TIMESTAMP) + '	EVERYTHING SEEMS FINE	IP : {3} ({2}, {0}, {1})\n'.format(region,country,city,IP))
	file_object.close()

# ping host url ----------------------------------------------------------------------------------
host = 'www.google.com'
if DEBUG == 1: print(str(TIMESTAMP)+' DEBUG: Pinging google')
try:
	ping = subprocess.Popen(
		['ping', '-c', '4', host],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)
except:
	if DEBUG == 1: print(f'			   DEBUG: Error while pinging (1): {e}')
	reason = 'Exception while pinging Google. Device likely offline.'
	offline(reason)
ping, error = ping.communicate()
# 'ping' is the result of the ping command now
if OFFLINEIDENT in str(ping):
	try:
		if DEBUG == 1: print(f'			   DEBUG: Error while pinging (2): {e}')
		reason = 'Exception while pinging google [2]. Device likely offline.'
		offline(reason)
	except Exception as e:
		if DEBUG == 1: print(f'			   DEBUG: Error while pinging (3): {e}')
		reason = 'Exception while pinging google [3]. Device likely offline.'
		offline(reason)
else:
	if DEBUG == 1: print('			   DEBUG: Ping successful')
	x = online()