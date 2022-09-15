import os
import subprocess
import sys
import traceback
from datetime import datetime

from zm_lib import raise_error, Settings, zabbix_sender, get_logger


def main(settings, logger):
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
        raise_error(settings, logger, "Too many arguments")
    elif len(sys.argv) < 2:
        raise_error(settings, logger, "Executed process not specified")
    process = sys.argv[1]
    # Execute process
    logger.info(f"Start process {process}")
    mine_time = datetime.now()
    result = execute_cmd(process)
    time_execution = round((datetime.now() - mine_time).total_seconds())
    logger.info(f"Process executed in {time_execution} sec.")
    # Send Zabbix info
    if settings.ZM_ZABBIX_SEND:
        try:
            zabbix_sender(settings, logger, result)
        except Exception:
            raise_error(settings, logger, "zm.py cannot send data to zabbix")
    exit(0)


def get_settings():
    settings = {}
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
    return settings


def execute_cmd(cmd, cwd_=None):
    result = 0
    try:
        # output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, )
        completed_process = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd_)
    except subprocess.CalledProcessError as exc:
        result = settings.ZM_ZABBIX_NOT_OK
        raise_error(settings, logger, f"Process '{cmd}' ended with error: code={exc.returncode}; error={exc.stderr}", do_error_exit=False)
    else:
        result = settings.ZM_ZABBIX_OK
        # out = output.decode("utf-8")
        logger.info(f'{completed_process.stdout}')
    return result


if __name__ == '__main__':

    # Get app settings
    try:
        settings = get_settings()
    except:
        print(f"ERROR: zm.py cannot get settings\n{traceback.format_exc()}")
        exit(1)

    # Create app logger
    try:
        logger = get_logger(settings)
        logger.debug(settings)
    except:
        print(f"ERROR: zm.py cannot get logger\n{traceback.format_exc()}")
        exit(1)

    # MAIN
    try:
        main(settings, logger)
    except:
        raise_error(settings, logger, f"{traceback.format_exc()}")
