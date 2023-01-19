# Raspberry-UpCheckerMini v1.4
# Intended as part of Raspberry-UpCheck
# 	github.com/induna-crewneck/Raspberry-UpCheck/
# This script is intended to check VPN connection integrity.
# On fail, it will run the full UpChecker script, which will log, notify the user and reboot
# This script can be cronjobbed to run very frequently. Suggested entry:
#	1 * * * * sudo python3 /root/Raspberry-UpCheck/UpCheckerMini.py >> /root/Raspberry-UpCheck/UpCheckerMiniLog.txt
# python3

# define process here that shouldn't run without VPN:
dangerousprocess = "qbittorrent"
VPNCOUNTRY = "US"

# imports ----------------------------------------------------------------------------------------
import os
import json
import urllib.request
import datetime

# define variables -------------------------------------------------------------------------------
dangerousprocess = str(dangerousprocess)
killcommand = "systemctl stop "+dangerousprocess
TIME = datetime.datetime.now()

# define functions -------------------------------------------------------------------------------
def killproc():
	RESPONSECODE = os.system(killcommand)
	if RESPONSECODE == 0: print(TIME,dangerousprocess,"stopped successfully")
	else:
		if RESPONSECODE == 128: print(TIME,"Invalid argument to exit")
		else:
			if 128 in RESPONSECODE: print(TIME,"Fatal error signal",RESPONSECODE)

def netwstate():
	# Get IP address and IP info
	url = 'http://ipinfo.io/json'
	response = urllib.request.urlopen(url)
	data = json.load(response)
	country = data['country']
	return(country)

# executing stuff --------------------------------------------------------------------------------
if str(netwstate()) == VPNCOUNTRY:
	# print(TIME,"Server is online and VPN is active.")
	# commented out to not blow up LogFile
	exit()
else:
	print(TIME,"Server is online, VPN is inactive.")
	killproc()
	os.system("python3 /root/Raspberry-UpCheck/UpChecker.py")