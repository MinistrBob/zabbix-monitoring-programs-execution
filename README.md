# zabbix-monitoring-programs-execution
The program controls the execution of any programs, scripts or commands OS and sends the execution result to zabbix, and in case of an execution error, it additionally can notify via telegram.  

NOTE: Any program that is controlled by a script in the future, I will call the process.  

## Work logic
Logging is done in stdout.  
All program settings are performed through environment variables.  
Telegram notifications can be turned off with `ZM_TELEGRAM_NOTIF=False`. In this case, you will only receive alerts from Zabbix in which you can also set up Telegram alerts, but zm.py has more informative alerts.  
Send data to can be turned off with Zabbix `ZM_ZABBIX_SEND=False`. In this case, you will only receive alerts to Telegram.
Send process time execution to can be turned off with Zabbix `ZM_ZABBIX_SEND_TIME=False`.
Only error messages are sent to Telegram. Messages about the successful completion of the process are not sent to Telegram (so that there is no flood).  
In case of successful completion of the process, the process execution time and the successful result are sent to Zabbix. The value of successful result is set to ZM_ZABBIX_OK.    
In case of the process execution error, execution time = 0 and the unsuccessful result are sent to Zabbix. The value of unsuccessful result is set to ZM_ZABBIX_NOT_OK.    

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

