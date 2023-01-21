# Raspberry-UpCheck

This pack of scripts has three purposes:

1) Check if the Raspberry Pi is online. Reboot if not.

2) Check if the VPN connection is established (by checking the location of the device's public IP). Reboot if not.

3) Notifying the user about the state of the connection (online & location) aswell as when the system reboots to signal that there may have been an issue. This is done via Telegram.

The provided scripts are tailored to my personal preferences. They will log the checks to a textfile, send updates via telegram and also notify via telegram on reboot. You can use it as basis to create your own script. If you want to use my script, follow the Installation steps below.

## What do the scripts do?

**UpChecker.py** is the core of the project. It will ping google.com to check if the device is online. If it is offline, it will log this and reboot the system. If it is online, it will get the country associated with the public IP of the device (using ipinfo.io). This country will be checked to see if it matches a user-defined 'BADCOUNTRY'. If you're using a VPN your BADCOUNTRY is your own real life country code. If you're not using a VPN or don't want to use this functionality, just set this to be any country that isn't your own/the one targeted by your VPN.
If it matches BADCOUNTRY, it will log this, reboot the system and notify the user via Telegram. If it doesn't match it will still log and notify but not reboot. It is intended to be set up to run every few hours via crobtab.

**BootNotifier.py** is an add-on that is meant to be set up to run on every system boot via crontab. It will notify the user about a reboot (for the case that the device was offline and has been rebooted by UpChecker.py) and also run UpChecker.py to check if the connection is as it should be (for the case that the device has been rebooted due to VPN failure).

**UpCheckerMini.py** is an add-on that is meant to run more frequently than UpChecker.py and not spam the user's Telegram. It only checks the VPN integrity. This time by checking if VPNCOUNTRY matches the device's public IP's location. If it does it does nothing, If it doesn't it will log this separately, kill a user-defined "dangerousprocess" that shouldn't run without a VPN and launch UpChecker.py to handle notifying the user and rebooting. This is not done by this script natively to keep the code as short and light as possible due to the intended high execution rate.

If you want to create your own version of the script, you can consult the CodeSnippets file for code I used, so you can mix and match.

This guide and the code used assumes you're doing this as root user. Mileage may vary using another user, code may need to be changed and sudo may have to be used.

### The main version is now running on Python 3.

I uploaded the old versions that ran under 2.7, but those will not be maintained.

## Dependencies
* python3
* python3 modules: subprocess, requests, os, re, json, urllib.request, datetime
* git (if you want to pull directly)

## Installation
To install the script, make sure 'git' is installed.

### Full code stack:
This will remove previous installations, install the code, set up the Telegram notifier and schedule the main script to run every 3h and the mini script to run every 5 minutes.

You need to enter your individual preferences and info before running it, though;
* Enter your Telegram Bot token where it says {ENTER YOUR TELEGRAM BOT TOKEN HERE} ( also replace the {} )
* Enter your Telegram user ID in the same fashion
* Define your BADCOUNTRY. This is the country you are located in (or any other NOT YOUR OWN country if you don't use a VPN or don't need this function)
* Define your VPNCOUNTRY. This is the country your VPN is set up to connect to (or your own country if you don't use a VPN or don't need this function)
* Define your PROCESS that you don't want to run without VPN. Use the bane you would use in a "systemctl status PROCESS" command

Optionally you can also adjust the crontab code (line before first 'fi') to adjust the intervall in which the code should run. Just make sure you escape any asterisks with \. More info on the crontab formatting further below.

```
rm -r /root/Raspberry-UpCheck/
git clone https://github.com/induna-crewneck/Raspberry-UpCheck.git
chmod 777 /root/Raspberry-UpCheck/UpCheckerLog.txt
chmod 777 /root/Raspberry-UpCheck/UpCheckerMiniLog.txt
perl -i -pe 's/telegram_bot_token/{ENTER YOUR TELEGRAM BOT TOKEN HERE}/g' /root/Raspberry-UpCheck/UpChecker.py
perl -i -pe 's/target_telegram_user_id/{ENTER YOUR TELEGRAM USER ID HERE}/g' /root/Raspberry-UpCheck/UpChecker.py
perl -i -pe 's/telegram_bot_token/{ENTER YOUR TELEGRAM BOT TOKEN HERE}/g' /root/Raspberry-UpCheck/BootNotifier.py
perl -i -pe 's/target_telegram_user_id/{ENTER YOUR TELEGRAM USER ID HERE}/g' /root/Raspberry-UpCheck/BootNotifier.py
perl -i -pe 's/badcountrycode/{ENTER YOUR BADCOUNTRY}/g' /root/Raspberry-UpCheck/UpChecker.py
perl -i -pe 's/goodcountrycode/{ENTER YOUR VPNCOUNTRY}/g' /root/Raspberry-UpCheck/UpCheckerMini.py
perl -i -pe 's/your_process_name/{ENTER YOUR PROCESS NAME}/g' /root/Raspberry-UpCheck/UpCheckerMini.py
if grep -q UpChecker.py "/var/spool/cron/crontabs/root"; then
	echo "UpChecker is already scheduled"
	else echo "0 \*/3 \* \* \* python /root/Raspberry-UpCheck/UpChecker.py" >> /var/spool/cron/crontabs/root
if grep -q UpCheckerMini.py "/var/spool/cron/crontabs/root"; then
	echo "UpCheckerMini is already scheduled"
	else echo "*/5 * * * * sudo python3 /root/Raspberry-UpCheck/UpCheckerMini.py >>/root/Raspberry-UpCheck/UpCheckerMiniLog.txt" >> /var/spool/cron/crontabs/root
fi
if grep -q BootNotifier.py "/var/spool/cron/crontabs/root"; then
	echo "BootNotifier is already scheduled"
	else echo "@reboot python /root/Raspberry-UpCheck/BootNotifier.py" >> /var/spool/cron/crontabs/root
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
Also define your BADCOUNTRY by replacing 'badcountrycode' with the countrycode of your real-life location.

Do the same for BootNotifier.py
```
nano /root/Raspberry-UpCheck/BootNotifier.py
```
Lastly edit UpCheckerMini.py
```
nano /root/Raspberry-UpCheck/UpChecker.py
```
Here you need to define your VPNCOUNTRY by replacing 'goodcountrycode' with the countrycode your VPN is targeting.

#### 3. Make log files writeable
```
chmod 777 /root/Raspberry-UpCheck/UpCheckerLog.txt
chmod 777 /root/Raspberry-UpCheck/UpCheckerMiniLog.txt
```

#### 4. (Optional) Run
To manually run the scripts (really only useful for or debugging/testing):
```
python3 /root/Raspberry-UpCheck/UpChecker.py
python3 /root/Raspberry-UpCheck/UpCheckerMini.py
python3 /root/Raspberry-UpCheck/BootNotifier.py
```
If you want to see if the scripts were run via crontab, you can use journalctl. Examples:
```
journalctl --identifier=CRON --grep="UpChecker" --since "1 hour ago"
journalctl --identifier=CRON --grep="BootNotifier"
```

#### 5. Automate
To periodically run the script:
```
crontab -e
```
add the following lines at the end of the file:
```
0 */3 * * * sudo python3 /root/Raspberry-UpCheck/UpChecker.py
*/5 * * * * sudo python3 /root/Raspberry-UpCheck/UpCheckerMini.py >>/root/Raspberry-UpCheck/UpCheckerMiniLog.txt
@reboot python3 /root/Raspberry-UpCheck/BootNotifier.py
```
(I think 'sudo' is needed here. I had it set up without it previously and it didn't reboot. You can cut the internet connection and see if it rebooted with 'uptime' command.)
Also, if you're wondering why UpCheckerMini.py has the output redirect (>>), this is the way it logs errors and events. This method keeps the code lighter.

Save the file and exit editor. cron should give a message that it has been updated.

This setting executes the main script every 3 hours. To change the time interval, replace the 60 in the code with whatever minute-intervall you prefer. The mini script runs every 5 minutes, this can also be adjusted.

You can test and generate the crontab intervall code [here](https://crontab.guru/). For example, running every 30 minutes would be '*/30 * * * * '

Cron jobs use the system's timezone and start at 00:00, so every 3h means it will run at 3am, 6am, 9am, 12pm, 3pm, 6pm, 9pm, 12am. The site linked above also shows you the next scheduled run based on your cron code.

### Uninstall
To delete the script, simply run
```
rm -r /root/Raspberry-UpCheck/
```
and delete the added lines in 'crontab -e'

### To do:
* Make an installer that automates and streamlines full-stack installation.

#### Sources:
https://stackoverflow.com/questions/316866/ping-a-site-in-python
https://forums.raspberrypi.com/viewtopic.php?t=39344
https://www.w3schools.com/python/ref_requests_post.asp
https://stackoverflow.com/questions/28669459/how-to-print-variables-without-spaces-between-values
https://stackabuse.com/python-check-if-string-contains-substring/
https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
