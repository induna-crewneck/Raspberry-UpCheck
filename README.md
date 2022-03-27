# Raspberry-UpCheck

Checking if Raspberry Pi is online periodically. Rebooting if not. The provided script is tailored to my personal preferences. It will log the checks to a textfile and send updates via telegram and also notify via telegram on reboot. You can use it as basis to create your own script. If you want to use my script, follow the Installation steps below.

If you want to create your own version of the script, you can consult the CodeSnippets file for code I used, so you can mix and match.

This guide and the code used assumes you're doing this as root user. Mileage may vary using another user, code may need to be changed and sudo may have to be used.

## Dependencies
* python
* git (if you want to pull directly)

## Installation
To install the script, make sure 'git' is installed.

### Full code stack:
This will remove previous installations, install the code, set up the Telegram notifier and schedule the script to run every 3h.
Just enter your telegram bot token and user id where indicated (remove the {}) and you will be set.
Optionally you can also adjust the crontab code (line before 'fi') to adjust the intervall in which the code should run. Just make sure you escape any asterisks with \.
```
rm -r /root/Raspberry-UpCheck/
git clone https://github.com/induna-crewneck/Raspberry-UpCheck.git
chmod 777 /root/Raspberry-UpCheck/UpCheckerLog.txt
perl -i -pe 's/telegram_bot_token/{ENTER YOUR TELEGRAM BOT TOKEN HERE}/g' /root/Raspberry-UpCheck/UpChecker.py
perl -i -pe 's/target_telegram_user_id/{ENTER YOUR TELEGRAM USER ID HERE}/g' /root/Raspberry-UpCheck/UpChecker.py
perl -i -pe 's/telegram_bot_token/{ENTER YOUR TELEGRAM BOT TOKEN HERE}/g' /root/Raspberry-UpCheck/BootNotifier.py
perl -i -pe 's/target_telegram_user_id/{ENTER YOUR TELEGRAM USER ID HERE}/g' /root/Raspberry-UpCheck/BootNotifier.py
if grep -q UpChecker.py "/var/spool/cron/crontabs/root"; then
	echo UpChecker is already scheduled
	else echo 0 \*/3 \* \* \* python /root/Raspberry-UpCheck/UpChecker.py >> /var/spool/cron/crontabs/root
	     echo @reboot /root/Raspberry-UpCheck/BootNotifier.py >> /var/spool/cron/crontabs/root
fi
```

### Step by Step

#### 1. Clone the Git Repo:
```
git clone https://github.com/induna-crewneck/Raspberry-UpCheck.git
```
This will download the files in this repo to '/root/Raspberry-UpCheck'

#### 2. Configure the script with your telegram data
```
nano /root/Raspberry-UpCheck/UpChecker.py
```
In lines 15 & 16 insert your telegram bot token and your user ID respectively.
([How to create a Telegram bot and get that token](https://core.telegram.org/bots))
To find out your user ID you can find @userinfobot on Telegram and text it /start.

Do the same for BootNotifier.py
```
nano /root/Raspberry-UpCheck/BootNotifier.py
```

#### 3. Make log file writeable
```
chmod 777 /root/Raspberry-UpCheck/UpCheckerLog.txt
```

#### 4. (Optional) Run
To manually run the script (really only useful for or debugging):
```
python /root/Raspberry-UpCheck/UpChecker.py
```

#### 5. Automate
To periodically run the script:
```
crontab -e
```
add the following lines at the end of the file:
```
0 */3 * * * sudo python /root/Raspberry-UpCheck/UpChecker.py
@reboot python /root/Raspberry-UpCheck/BootNotifier.py
```
(I think 'sudo' is needed here. I had it set up without it previously and it didn't reboot. You can cut the internet connection and see if it rebooted with 'uptime' command.

Save the file and exit editor. cron should give a message that it has been updated.

This setting executes the script every 3 hours. To change the time interval, replace the 60 in the code with whatever minute-intervall you prefer.

You can test and generate the crontab intervall code [here](https://crontab.guru/). For example, running every 30 minutes would be '*/30 * * * * '

Cron jobs use the system's timezone and start at 00:00, so every 3h means it will run at 3am, 6am, 9am, 12pm, 3pm, 6pm, 9pm, 12am. The site linked above also shows you the next scheduled run based on your cron code.

### Uninstall
To delete the script, simply run
```
rm -r /root/Raspberry-UpCheck/
```
and delete the added lines in 'crontab -e'


#### Sources:
https://stackoverflow.com/questions/316866/ping-a-site-in-python
https://forums.raspberrypi.com/viewtopic.php?t=39344
https://www.w3schools.com/python/ref_requests_post.asp
https://stackoverflow.com/questions/28669459/how-to-print-variables-without-spaces-between-values
https://stackabuse.com/python-check-if-string-contains-substring/
https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
