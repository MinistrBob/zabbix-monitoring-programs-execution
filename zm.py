import os
import logging
import os
import shutil
import sys
import traceback
from urllib import request, parse
from datetime import datetime
from pyzabbix import ZabbixAPI

# Program settings
settings = {}
# Program logger
logger = logging.getLogger()
# Executed process
process = ""


def main():
    global process
    # Get app settings
    try:
        get_settings()
    except Exception as exc:
        print(f"ERROR: zm.py cannot get settings\n{exc.returncode}\n{exc.output}")
        exit(1)
    # Create app logger
    set_logger()
    logger.debug(settings)
    # Check required setting
    if settings.ZM_TELEGRAM_NOTIF and \
            (not settings.ZM_TELEGRAM_BOT_TOKEN or not settings.ZM_TELEGRAM_CHAT):
        print(f"ERROR: Telegram notifications are enabled but the parameters ZM_TELEGRAM_BOT_TOKEN, ZM_TELEGRAM_CHAT "
              f"are not defined\n{exc.returncode}\n{exc.output}")
        exit(1)
    if settings.ZM_ZABBIX_SEND and \
            (not settings.ZM_ZABBIX_URL or not settings.ZM_ZABBIX_USER or not settings.ZM_ZABBIX_PASSWORD):
        print(f"ERROR: Send data to Zabbix are enabled but the parameters ZM_ZABBIX_URL, ZM_ZABBIX_USER, "
              f"ZM_ZABBIX_PASSWORD are not defined\n{exc.returncode}\n{exc.output}")
        exit(1)
    # Check app arguments
    if len(sys.argv) > 2:
        raise_error("Too many arguments", AttributeError)
    elif len(sys.argv) < 2:
        raise_error("Executed process not specified", AttributeError)
    process = sys.argv[1]
    # Connect to Zabbix server
    try:
        zapi = ZabbixAPI(url=settings.ZM_ZABBIX_URL, user=settings.ZM_ZABBIX_USER, password=settings.ZM_ZABBIX_PASSWORD)
    except Exception as exc:
        raise_error("zm.py cannot connect to Zabbix", exc)
    # Execute process
    logger.info(f"Start process {process}")
    mine_time = datetime.now()
    execute_cmd(process, message_prefix=message_prefix)
    logger.info(f"Process executed in {datetime.now() - mine_time} sec.")
    # Send Zabbix info
    if settings.ZM_ZABBIX_SEND:
        pass
        # TODO: Send data to Zabbix


def raise_error(message, exc):
    message = f"<b>ERROR</b>: {message}"
    trace = f"<b>ERROR</b>: <b>returncode</b>={exc.returncode}; <b>output</b>:\n{exc.output}"
    logger.error(message)
    logger.error(trace)
    if settings.ZM_TELEGRAM_NOTIF:
        message = f"""❌ <b>zm.py</b> from <b>{settings.HOSTNAME}</b>
Error during process execution <code>{process}</code>
{message}
{trace}"""
        telegram_notification(message)
    exit(1)


def telegram_notification(message):
    params = {
        'chat_id': settings.ZM_TELEGRAM_CHAT,
        'disable_web_page_preview': '1',
        'parse_mode': 'HTML',
        'text': message
    }
    logger.debug(params)
    data = parse.urlencode(params).encode()
    logger.debug(data)
    req = request.Request(f"https://api.telegram.org/bot{settings.ZM_TELEGRAM_BOT_TOKEN}/sendMessage", data=data)
    logger.debug(req)
    resp = request.urlopen(req)
    logger.debug(resp)
    return resp


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
    settings['ZM_DEBUG'] = os.getenv('ZM_DEBUG', False)
    settings['HOSTNAME'] = os.getenv('HOSTNAME', "Unknown")
    # settings['ZM_LOG_DIR'] = os.getenv('ZM_LOG_DIR', os.path.abspath(os.path.dirname(__file__)))
    # Should app send telegram alerts? or log messages only to stdout.
    settings['ZM_TELEGRAM_NOTIF'] = os.getenv('ZM_TELEGRAM_NOTIF', True)

    # Zabbix settings
    # Should app send data to Zabbix?
    settings['ZM_ZABBIX_SEND'] = os.getenv('ZM_ZABBIX_SEND', True)
    # OK value for Zabbix
    settings['ZM_ZABBIX_OK'] = os.getenv('ZABBIX_OK', 0)
    # Not OK value for Zabbix
    settings['ZM_ZABBIX_NOT_OK'] = os.getenv('ZM_ZABBIX_NOT_OK', 1)
    settings['ZM_ZABBIX_URL'] = os.getenv('ZM_ZABBIX_URL', None)
    settings['ZM_ZABBIX_USER'] = os.getenv('ZM_ZABBIX_USER', None)
    settings['ZM_ZABBIX_PASSWORD'] = os.getenv('ZM_ZABBIX_PASSWORD', None)

    # Telegram settings
    # Telegram connection timeout
    settings['ZM_TELEGRAM_TIMEOUT'] = os.getenv('ZM_TELEGRAM_TIMEOUT', 10)
    # Telegram AUTH
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


def execute_cmd(cmd, cwd_=None, message=None, message_prefix=None, output_prefix=None):
    if not message_prefix:
        message_prefix = ""
    if not output_prefix:
        output_prefix = ""
    if message:
        logger.info(f"{message_prefix}{message}")
    else:
        logger.info(f"{message_prefix}{cmd}")
    try:
        # output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, )
        completed_process = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd_)
    except subprocess.CalledProcessError as exc:
        raise_error("Process ended with error", exc)
    else:
        # out = output.decode("utf-8")
        logger.info(f'{output_prefix}{completed_process.stdout}')


if __name__ == '__main__':
    main()
