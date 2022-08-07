# zabbix-monitoring-programs-execution
The program controls the execution of programs, scripts or commands OS (any program, scripts and command) and sends the execution result to zabbix, and in case of an execution error, it additionally can notify via telegram.  

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

