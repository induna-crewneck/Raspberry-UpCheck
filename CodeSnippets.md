# Code snippets

## These are just code snippets that were used for this project or may otherwise be useful

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
## Unused functions
### Getting state of process
Theis was written for UpCheckerMini but not included in the final version to keep the code light. It would have been used to check if it's running before attempting to stop it.
```
statuscommand = "systemctl status "+processname

def procstate():
	PROCESSSTATUS = os.popen(statuscommand).read()
	if "Active: inactive" in PROCESSSTATUS:
		return("dead")
	else:
		return("alive")
```
