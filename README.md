# Raspberry-UpCheck

Checking if Raspberry Pi is online periodically. Rebooting if not.

To check online status Google will be pinged.

## Installation
To periodically run the script:
In the console type in 'sudo crontab -e' and add the following line at the end of the file:
*/10 * * * * python /home/path/to/script.py
Save the file and exit editor. cron should give a message that it has been updated.

This setting executes the script every 10 minutes.

## Useful code snippets
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
Failure result of ping:
'100% packet loss'

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
