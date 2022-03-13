# Raspberry-UpCheck

Checking if Raspberry Pi is online periodically. Rebooting if not. The provided script is tailored to my personal preferences. It will log the checks to a textfile and send updates via telegram. You can use it as basis to create your own script. If you want to use my script, follow the Installation steps below.

If you want to create your own version of the script, further down on this page are the code snippets used, so you can mix and match.

## Dependencies
* python
* git (if you want to pull directly)

## Installation
To install the script, make sure 'git' is installed.

### Clone the Git Repo:
```
git clone https://github.com/induna-crewneck/Raspberry-UpCheck.git
```
This will download the files in this repo to '/root/Raspberry-UpCheck'

### Configure the script with your telegram data
```
nano /root/Raspberry-UpCheck/UpChecker.py
```
In lines 15 & 16 insert your telegram bot token and your user ID respectively.
([How to create a Telegram bot and get that token](https://core.telegram.org/bots))
To find out your user ID you can find @userinfobot on Telegram and text it /start.

### Make log file writeable
```
chmod 777 /root/Raspberry-UpCheck/UpCheckerLog.txt
```

### Run
To manually run the script (really only useful for or debugging):
```
python /root/Raspberry-UpCheck/UpChecker.py
```

### Automate
To periodically run the script:
```
sudo crontab -e
```
add the following line at the end of the file:
```
*/60 * * * * python /root/Raspberry-UpCheck/UpChecker.py
```
Save the file and exit editor. cron should give a message that it has been updated.

This setting executes the script every 60 minutes. To change the time interval, replace the 60 in the code with whatever minute-intervall you prefer.

### Uninstall
To delete the script, simply run
```
m -r /root/Raspberry-UpCheck/
```
and delete the added line in 'crontab -e'





# Code snippets
### Ping URL in python and print (show) ping resut
```
import subprocess
# ping host url ----------------------------------
host = "www.google.com"
ping = subprocess.Popen(
    ["ping", "-c", "4", host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)
ping, error = ping.communicate()
# echo ping results ------------------------------
print ping
```
Interpretation of results:
'0% packet loss'                            in 'ping'   means success       ('error' is empty)
'Temporary failure in name resolution'      in 'error'  means no connection ('ping' is empty)

### Search string for substring
```
string = "wordstringword"
substring = "string"

if substring in string:
    print("Found!")
else:
    print("Not found!")

```

### Reboot system
Syntax can be used to send any command
```
import os
os.system('reboot')
```

### Get IP and store as variable
```
IP = os.popen('curl icanhazip.com').read()
```
#### Get detailed IP info
```
import re
import json
from urllib2 import urlopen

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

IP=data['ip']
org=data['org']
city = data['city']
country=data['country']
region=data['region']

print 'Your IP detail\n '
print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP)
```

### Send telegram message
Requires Telegram Bot Token. See [here](https://core.telegram.org/bots) for more info.

Install dependencies:
```
pip install requests
```
python code:
```
import requests
# define Variables -------------------------------
TELEGRAM_BOT = 'telegram_bot_token_token'
TELEGRAM_ME  = 'personal_telegram_user_id'
TELEGRAM_MSG = 'messagecontent'
# URL POST ---------------------------------------
url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
myobj = {'somekey': 'somevalue'}
x = requests.post(url, data = myobj)
# Print response text of POST request ------------
print(x.text)
```
### Get Date and Time
```
import datetime
print datetime.datetime.now()
```


#### Sources:
https://stackoverflow.com/questions/316866/ping-a-site-in-python
https://forums.raspberrypi.com/viewtopic.php?t=39344
https://www.w3schools.com/python/ref_requests_post.asp
https://stackoverflow.com/questions/28669459/how-to-print-variables-without-spaces-between-values
https://stackabuse.com/python-check-if-string-contains-substring/
https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
