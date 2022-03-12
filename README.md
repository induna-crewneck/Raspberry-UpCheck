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
### Send telegram message
```
import requests
# define Variables -------------------------------
TELEGRAM_BOT = 'telegram_bot_token_token'
TELEGRAM_ME  = 'personal_telegram_user_id'
TELEGRAM_MSG = 'messagecontent'
# URL POST ---------------------------------------
url = 'https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage?chat_id={TELEGRAM_ME}&text={TELEGRAM_MSG}'
myobj = {'somekey': 'somevalue'}
x = requests.post(url, data = myobj)
# Print response text of POST request ------------
print(x.text)
```



#### Sources:
https://stackoverflow.com/questions/316866/ping-a-site-in-python
https://forums.raspberrypi.com/viewtopic.php?t=39344
https://www.w3schools.com/python/ref_requests_post.asp
