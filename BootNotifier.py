# Raspberry-BootNotifier v1.0
# Intended as part of Raspberry-UpCheck
# github.com/induna-crewneck/Raspberry-UpCheck/
# python

# define Variables -------------------------------------------------------------------------------
TELEGRAM_BOT = 'telegram_bot_token'
TELEGRAM_ME  = 'target_telegram_user_id'
TELEGRAM_MSG = 'empty message'
TIMESTAMP = datetime.datetime.now()

# Get IP address and IP info
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
IP=data['ip']
city = data['city']
country=data['country']
region=data['region']
    
# Sending update message via Telegram
TELEGRAM_MSG='Pi is online (routine check) \n'+ str(TIMESTAMP) + ' \nIP : {3} \n({2}, {0}, {1})'.format(region,country,city,IP)
url = 'https://api.telegram.org/bot' + str(TELEGRAM_BOT) + '/sendMessage?chat_id=' + str(TELEGRAM_ME) + '&text=' + str(TELEGRAM_MSG)
y = requests.post(url)
# 'y' is now the reponse of sending the telegram message
# show detailed reponse:    print y.text
# show response code:       print y
    
# Logging to OnlineStatusLog.txt
file_object = open('Raspberry-UpCheck/UpCheckerLog.txt', 'a')
file_object.write(' \n-------------------------------------------------------------------------------------------------------- \n' + str(TIMESTAMP) + '    SYSTEM REBOOTED    \nIP : {3} ({2}, {0}, {1})'.format(region,country,city,IP))
file_object.close()
