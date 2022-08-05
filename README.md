# zabbix-monitoring-programs-execution
The program controls the execution of other programs and sends the execution result to zabbix, and in case of an execution error, it additionally notifies via telegram.  

## For developers
### Get requirements.txt
`pip freeze | Out-File -Encoding UTF8 c:\MyGit\zabbix-monitoring-programs-execution\requirements.txt`  
`pip install -r c:\MyGit\zabbix-monitoring-programs-execution\requirements.txt`  