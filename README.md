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
| ENV | Default | Description |
|----------|------|-------------------------------------|
| `ZM_DEBUG` | `False` | Enable DEBUG mode? (True or False). |
| `HOSTNAME` | `Unknown` | For Telegram message to see which host this message is from. In Linux, such a variable is usually already set. |
| Zabbix settings |||
| `HOSTNAME` | `Unknown` | For Telegram message to see which host this message is from. In Linux, such a variable is usually already set. |
| `ZM_ZABBIX_SEND` | `True` | Should app send data to Zabbix? (True or False). |
| `ZM_ZABBIX_SEND_TIME` | `True` | Should app send execution time to Zabbix? (True or False). |
| `ZM_ZABBIX_OK` | `0` | OK value for Zabbix. |
| `ZM_ZABBIX_NOT_OK` | `1` | Not OK value for Zabbix. |
| `ZM_ZABBIX_IP` | `None` | Zabbix server ip address. |
| `ZM_ZABBIX_HOST_NAME` | `None` | Zabbix "Host name". How is the host named in Zabbix. |
| `ZM_ZABBIX_ITEM_NAME` | `None` | How is the trapped item key named in Zabbix. |
| `ZM_ZABBIX_ITEM_TIME_NAME` | `None` | How is the trapped item for execution time key named in Zabbix. |
| Telegram settings |||
| `ZM_TELEGRAM_NOTIF` | `True` | Should app send telegram alerts? or log messages only to stdout. (True or False). |
| `ZM_TELEGRAM_TIMEOUT` | `10` | Telegram connection timeout. |
| `ZM_TELEGRAM_BOT_TOKEN` | `None` | Telegram bot token. It usually looks like this `1470616475:AAHFSvznxxLTDedQBSiRVrYVP49ixkghpRT`. You need to create a bot in Telegram using [BotFather](https://t.me/BotFather) and you can also get a bot token there. |
| `ZM_TELEGRAM_CHAT` | `None` | Telegram chat (ID) to which the bot will send messages. If this is a private chat, then usually the ID looks like a positive number. If it is a channel or group then ID is a negative number. |

## Install and run
### Customize Zabbix
Create trapped items `ZM_ZABBIX_ITEM_NAME` and if you need `ZM_ZABBIX_ITEM_TIME_NAME`


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

