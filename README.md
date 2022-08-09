# zabbix-monitoring-programs-execution
The program controls the execution of any programs, scripts or commands OS and sends the execution result to zabbix, and in case of an execution error, it additionally can notify via telegram.  

**NOTE**: Any programs, scripts or commands OS that is controlled by zm.py in the future, I will call - process.  

## Work logic
Logging is done in stdout.  
All zm.py settings are performed through environment variables.  
Telegram notifications can be turned off with `ZM_TELEGRAM_NOTIF=False`. In this case, you will only receive alerts from Zabbix in which you can also set up Telegram alerts, but zm.py has more informative alerts.  
Send data to can be turned off with Zabbix `ZM_ZABBIX_SEND=False`. In this case, you will only receive alerts to Telegram.
Send process time execution to can be turned off with Zabbix `ZM_ZABBIX_SEND_TIME=False`.
Only error messages are sent to Telegram. Messages about the successful completion of the process are not sent to Telegram (so that there is no flood).  
In case of successful completion of the process, the process execution time and the successful result are sent to Zabbix. The value of successful result is set to ZM_ZABBIX_OK.    
In case of the process execution error, execution time = 0 and the unsuccessful result are sent to Zabbix. The value of unsuccessful result is set to ZM_ZABBIX_NOT_OK.
You can run zm.py in a Docker container.

## Settings
| ENV | Default | Description                                                                                                                                                                                                             |
|----------|------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `ZM_DEBUG` | `False` | Enable DEBUG mode? (True or False).                                                                                                                                                                                     |
| `HOSTNAME` | `Unknown` | For Telegram message to see which host this message is from. In Linux, such a variable is usually already set.                                                                                                          |
| Zabbix settings |||
| `ZM_ZABBIX_SEND` | `True` | Should app send data to Zabbix? (True or False).                                                                                                                                                                        |
| `ZM_ZABBIX_SEND_TIME` | `True` | Should app send execution time to Zabbix? (True or False).                                                                                                                                                              |
| `ZM_ZABBIX_OK` | `0` | OK value for Zabbix.                                                                                                                                                                                                    |
| `ZM_ZABBIX_NOT_OK` | `1` | Not OK value for Zabbix.                                                                                                                                                                                                |
| `ZM_ZABBIX_IP` | `None` | Zabbix server ip address.                                                                                                                                                                                               |
| `ZM_ZABBIX_HOST_NAME` | `None` | Zabbix "Host name". How is the host named in Zabbix. (See picture after table).                                                                                                                                         |
| `ZM_ZABBIX_ITEM_NAME` | `None` | How is the trapped item key named in Zabbix.                                                                                                                                                                            |
| `ZM_ZABBIX_ITEM_TIME_NAME` | `None` | How is the trapped item for execution time key named in Zabbix.                                                                                                                                                         |
| Telegram settings |||
| `ZM_TELEGRAM_NOTIF` | `True` | Should app send telegram alerts? or log messages only to stdout. (True or False).                                                                                                                                       |
| `ZM_TELEGRAM_TIMEOUT` | `10` | Telegram connection timeout.                                                                                                                                                                                            |
| `ZM_TELEGRAM_BOT_TOKEN` | `None` | Telegram bot token. It usually looks like this `1470616475:AAHFSvznxxLTDedQBSiRVrYVP49ixkghpRT`. You need to create a bot in Telegram using [BotFather](https://t.me/BotFather) and you can also get a bot token there. |
| `ZM_TELEGRAM_CHAT` | `None` | Telegram chat (ID) to which the bot will send messages. If this is a private chat, then usually the ID looks like a positive number. If it is a channel or group then ID is a negative number.                          |

**NOTE**: Parameter `ZM_ZABBIX_HOST_NAME` you can see here  
![zabbix trapped item](https://github.com/MinistrBob/zabbix-monitoring-programs-execution/blob/main/static/zabbix-host-name.png?raw=true)

## Install and run
### Install Python3
[Python Download](https://www.python.org/downloads/)
### Customize Zabbix
In this example, `ZM_ZABBIX_ITEM_NAME` will be called `docker-rmi-sh` and `ZM_ZABBIX_ITEM_TIME_NAME` - `docker-rmi-sh-time`. This name will be written in the `Key` field.  
Create trapped items `ZM_ZABBIX_ITEM_NAME` and if you need `ZM_ZABBIX_ITEM_TIME_NAME`.  
![zabbix trapped item](https://github.com/MinistrBob/zabbix-monitoring-programs-execution/blob/main/static/zabbix-trapper-item.png?raw=true)
![zabbix trapped item execution time](https://github.com/MinistrBob/zabbix-monitoring-programs-execution/blob/main/static/zabbix-trapper-item-time.png?raw=true)
Create trigger for `ZM_ZABBIX_ITEM_NAME` with that Expression:  
`{172.26.12.168:docker-rmi-sh.last()}=1 or {172.26.12.168:docker-rmi-sh.nodata(25h)}<>0`  
The trigger fires when there was an error while executing the process or when the process has not run for more than 25 hours.  
![zabbix trapped item](https://github.com/MinistrBob/zabbix-monitoring-programs-execution/blob/main/static/zabbix-trigger.png?raw=true)
You can see Graphs for items: menu **Monitoring** - **Latest data** - **Filter.Hosts** choose desired host - there is **Graph** in the item line.  
Or you cat create your own graphs.  
![zabbix trapped item](https://github.com/MinistrBob/zabbix-monitoring-programs-execution/blob/main/static/latest-data.png?raw=true)
### Settings
You must set environment variables on the computer where the zm.py will run and under the account under which zm.py will run.   
There are many ways to define environment variables.  
### Run
In this example, I write all the necessary variables in file `.bash_profile`.  
```commandline
export ZM_ZABBIX_IP="172.26.12.86"
export ZM_ZABBIX_HOST_NAME="172.26.12.168"
export ZM_ZABBIX_ITEM_NAME="docker-rmi-sh"
export ZM_ZABBIX_ITEM_TIME_NAME="docker-rmi-sh-time"
export ZM_TELEGRAM_BOT_TOKEN="1470616475:AAHFSvznxxLTDedQBSiRVrYVP49ixkghpRT"
export ZM_TELEGRAM_CHAT="123456789"
```
#### 1) As script
```commandline
mkdir /usr/share/zabbix-monitoring-programs-execution
cd /usr/share/zabbix-monitoring-programs-execution
git clone https://github.com/MinistrBob/zabbix-monitoring-programs-execution.git .
pip3 install -r requirements.txt
python3 /usr/share/zabbix-monitoring-programs-execution/zm.py <process>
``` 
#### 2) As Docker container (RECOMMENDED)
```commandline
docker run --rm ministrbob/zabbix-monitoring-programs-execution:latest <process>
```
#### 3) As cronjob (or if you use sudo -s or su)
If you use cronjob or if you use sudo -s or su you will need `source` command
```commandline
* * * * * source /home/user/.bash_profile; python3 zm.py <process>
```

## For developers
### Get and install requirements (requirements.txt)
`pip freeze | Out-File -Encoding UTF8 c:\MyGit\zabbix-monitoring-programs-execution\requirements.txt`  
`pip install -r c:\MyGit\zabbix-monitoring-programs-execution\requirements.txt`  

### Telegram
[sendMessage](https://telegram-bot-sdk.readme.io/reference/sendmessage) `https://api.telegram.org/bot{token}/sendMessage`
Example message (html):
```html
MESSAGE: ❌ Test <b>bold</b>,
<strong>bold</strong>
<i>italic</i>, <em>italic</em>
<a href="URL">inline URL</a>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
```
### Build Docker image
You can take docker image here - `ministrbob/zabbix-monitoring-programs-execution:latest`.  
If you want run zm.py as docker container you can build docker image and push it to your own docker hub.  
```
docker login
docker build . -t ministrbob/zabbix-monitoring-programs-execution:latest
docker push ministrbob/zabbix-monitoring-programs-execution:latest
```
