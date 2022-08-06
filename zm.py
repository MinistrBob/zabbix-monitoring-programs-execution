import os
import logging
import os
import shutil
import sys
import traceback
from datetime import datetime
from pyzabbix import ZabbixAPI

# Program settings
settings = {}
# Program logger
logger = logging.getLogger()


def main():
    # Get app settings
    try:
        get_settings()
    except Exception as exc:
        msg = f"ERROR: zm.py cannot get settings\n{exc.returncode}\n{exc.output}"
        print(msg)
        telegram_notification(msg)
        exit(1)
    # Create app logger
    set_logger()
    logger.debug(settings)
    # Check app arguments
    if len(sys.argv) > 2:
        raise_error("Too many arguments", AttributeError)
    elif len(sys.argv) < 2:
        raise_error("Executed process not specified", AttributeError)
    process = sys.argv[1]
    # Connect to zabbix server
    try:
        zapi = ZabbixAPI(url=settings.ZM_ZABBIX_URL, user=settings.ZM_ZABBIX_USER, password=settings.ZM_ZABBIX_PASSWORD)
    except Exception as exc:
        raise_error("zm.py cannot connect to zabbix", exc)
    # Execute process
    logger.info(f"Start process {process}")
    mine_time = datetime.now()
    execute_cmd(process, message_prefix=message_prefix)
    logger.info(f"Process executed in {datetime.now() - mine_time} sec.")
    # Send zabbix info


def raise_error(message, exc):
    logger.error("ERROR: {message}")
    logger.error("ERROR:\n", exc.returncode, exc.output)
    # TODO: telegram message
    exit(1)


def telegram_notification(message):
    pass


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
    # settings['ZM_LOG_DIR'] = os.getenv('ZM_LOG_DIR', os.path.abspath(os.path.dirname(__file__)))
    # Zabbix settings
    # zabbix_sender binary
    # settings['ZM_ZABBIX_SENDER'] = os.getenv('ZM_ZABBIX_SENDER', "/usr/bin/zabbix_sender")
    # Zabbix agent configuration file
    # settings['ZM_ZABBIX_SENDER_CONF'] = os.getenv('ZM_ZABBIX_SENDER_CONF', "/etc/zabbix/zabbix_agentd.conf")
    # OK value for Zabbix
    settings['ZM_ZABBIX_OK'] = os.getenv('ZABBIX_OK', 0)
    # Not OK value for Zabbix
    settings['ZM_ZABBIX_NOT_OK'] = os.getenv('ZM_ZABBIX_NOT_OK', 1)
    settings['ZM_ZABBIX_URL'] = 'http://172.26.12.86'
    settings['ZM_ZABBIX_USER'] = 'bobrovsky'
    settings['ZM_ZABBIX_PASSWORD'] = '7#TS9$Vt#Ccu'

    settings = Settings(settings)


def set_logger():
    # Log to stdout
    global logger
    if settings.ZM_DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    stdout_log_formatter = logging.Formatter('%(asctime)s|%(levelname)8s| %(message)s')
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
    if not settings.dry_run:
        try:
            # output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, )
            completed_process = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd_)
        except subprocess.CalledProcessError as exc:
            raise_error("process ended with error", exc)
        else:
            # out = output.decode("utf-8")
            logger.info(f'{output_prefix}{completed_process.stdout}')


if __name__ == '__main__':
    main()
