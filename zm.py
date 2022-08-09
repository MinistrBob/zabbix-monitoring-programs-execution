import os
import logging
import os
import shutil
import sys
import traceback
import subprocess
from urllib import request, parse
from datetime import datetime
# from pyzabbix import ZabbixAPI
from pyzabbix import ZabbixMetric, ZabbixSender

# Program settings
settings = {}
# Program logger
logger = logging.getLogger()
# Executed process
process = ""
time_execution = 0
result = 0


def main():
    global process, time_execution
    # Get app settings
    try:
        get_settings()
    except Exception:
        print(f"ERROR: zm.py cannot get settings")
        exit(1)
    # Create app logger
    set_logger()
    logger.debug(settings)
    # Check required setting
    if settings.ZM_TELEGRAM_NOTIF and \
            (not settings.ZM_TELEGRAM_BOT_TOKEN or not settings.ZM_TELEGRAM_CHAT):
        print(f"ERROR: Telegram notifications are enabled but the parameters ZM_TELEGRAM_BOT_TOKEN, ZM_TELEGRAM_CHAT "
              f"are not defined")
        exit(1)
    if settings.ZM_ZABBIX_SEND and \
            (not settings.ZM_ZABBIX_IP or not settings.ZM_ZABBIX_HOST_NAME or not settings.ZM_ZABBIX_ITEM_NAME):
        print(f"ERROR: Send data to Zabbix are enabled but the parameters ZM_ZABBIX_IP, ZM_ZABBIX_HOST_NAME, "
              f"ZM_ZABBIX_ITEM_NAME are not defined")
        exit(1)
    # Check app arguments
    if len(sys.argv) > 2:
        raise_error("Too many arguments")
    elif len(sys.argv) < 2:
        raise_error("Executed process not specified")
    process = sys.argv[1]
    # Execute process
    logger.info(f"Start process {process}")
    mine_time = datetime.now()
    execute_cmd(process)
    time_execution = datetime.now() - mine_time
    logger.info(f"Process executed in {time_execution} sec.")
    # Send Zabbix info
    if settings.ZM_ZABBIX_SEND:
        try:
            zabbix_sender()
        except Exception:
            raise_error("zm.py cannot send data to zabbix")
    exit(0)


def raise_error(message, do_error_exit=True):
    logger.error(f"<b>ERROR</b>: {message}")
    telegram_message = f"""❌ <b>zm.py</b> from <b>{settings.HOSTNAME}</b>
Error during process execution <code>{process}</code>
{message}
"""
    telegram_notification(telegram_message)
    if do_error_exit:
        exit(1)


def zabbix_sender():
    global result
    metrics = []
    m = ZabbixMetric(settings.ZM_ZABBIX_HOST_NAME, settings.ZM_ZABBIX_ITEM_NAME, result)
    metrics.append(m)
    if settings.ZM_ZABBIX_SEND_TIME:
        m = ZabbixMetric(settings.ZM_ZABBIX_HOST_NAME, settings.ZM_ZABBIX_ITEM_TIME_NAME, time_execution)
        metrics.append(m)
    zbx = ZabbixSender(settings.ZM_ZABBIX_IP)
    zbx.send(metrics)


def telegram_notification(message):
    if settings.ZM_TELEGRAM_NOTIF:
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'
        # }
        params = {
            'chat_id': settings.ZM_TELEGRAM_CHAT,
            'disable_web_page_preview': '1',
            'parse_mode': 'HTML',
            'text': message
        }
        logger.debug(f"params={params}")
        data = parse.urlencode(params).encode()
        logger.debug(f"data={data}")
        url = f"https://api.telegram.org/bot{settings.ZM_TELEGRAM_BOT_TOKEN}/sendMessage"
        logger.debug(f"url={url}")
        # req = request.Request(url, data=data, method='POST', headers=headers)
        req = request.Request(url, data=data, method='POST')
        logger.debug(f"req={req}")
        resp = request.urlopen(req)
        logger.debug(f"resp={resp}")


class Settings(object):
    """
    Program settings like class
    """

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)

    def __str__(self):
        return str(self.__dict__)


def get_settings():
    global settings
    # Enable DEBUG mode?
    settings['ZM_DEBUG'] = os.getenv("ZM_DEBUG", 'False').lower() in 'true'
    # For Telegram message to see which host this message is from.
    settings['HOSTNAME'] = os.getenv('HOSTNAME', "Unknown")
    # settings['ZM_LOG_DIR'] = os.getenv('ZM_LOG_DIR', os.path.abspath(os.path.dirname(__file__)))

    # Zabbix settings
    # Should app send data to Zabbix?
    settings['ZM_ZABBIX_SEND'] = os.getenv("ZM_ZABBIX_SEND", 'True').lower() in 'true'
    # Should app send execution time to Zabbix?
    settings['ZM_ZABBIX_SEND_TIME'] = os.getenv("ZM_ZABBIX_SEND_TIME", 'True').lower() in 'true'
    # OK value for Zabbix.
    settings['ZM_ZABBIX_OK'] = os.getenv('ZABBIX_OK', 0)
    # Not OK value for Zabbix.
    settings['ZM_ZABBIX_NOT_OK'] = os.getenv('ZM_ZABBIX_NOT_OK', 1)
    # Zabbix server ip address.
    settings['ZM_ZABBIX_IP'] = os.getenv('ZM_ZABBIX_IP', None)
    # Zabbix "Host name". How is the host named in Zabbix.
    settings['ZM_ZABBIX_HOST_NAME'] = os.getenv('ZM_ZABBIX_HOST_NAME', None)
    # How is the trapped item key named in Zabbix.
    settings['ZM_ZABBIX_ITEM_NAME'] = os.getenv('ZM_ZABBIX_ITEM_NAME', None)
    # How is the trapped item for execution time key named in Zabbix.
    settings['ZM_ZABBIX_ITEM_TIME_NAME'] = os.getenv('ZM_ZABBIX_ITEM_TIME_NAME', None)

    # Telegram settings
    # Should app send telegram alerts? or log messages only to stdout.
    settings['ZM_TELEGRAM_NOTIF'] = os.getenv("ZM_TELEGRAM_NOTIF", 'True').lower() in 'true'
    # Telegram connection timeout.
    settings['ZM_TELEGRAM_TIMEOUT'] = os.getenv('ZM_TELEGRAM_TIMEOUT', 10)
    # Telegram AUTH.
    settings['ZM_TELEGRAM_BOT_TOKEN'] = os.getenv('ZM_TELEGRAM_BOT_TOKEN', None)
    settings['ZM_TELEGRAM_CHAT'] = os.getenv('ZM_TELEGRAM_CHAT', None)

    settings = Settings(settings)


def set_logger():
    # Log to stdout
    global logger
    if settings.ZM_DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    stdout_log_formatter = logging.Formatter('%(asctime)s|%(levelname)-5s|%(funcName)s| %(message)s')
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(stdout_log_formatter)
    logger.addHandler(stdout_handler)


def execute_cmd(cmd, cwd_=None):
    global result
    try:
        # output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, )
        completed_process = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd_)
    except subprocess.CalledProcessError as exc:
        result = settings.ZM_ZABBIX_NOT_OK
        raise_error(f"Process ended with error: code={exc.returncode}; error={exc.stderr}", do_error_exit=False)
    else:
        result = settings.ZM_ZABBIX_OK
        # out = output.decode("utf-8")
        logger.info(f'{completed_process.stdout}')


if __name__ == '__main__':
    main()
