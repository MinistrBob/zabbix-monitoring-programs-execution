import os
import logging
import os
import shutil
import sys
import traceback
from datetime import datetime

# Program settings
settings = {}
# Program logger
logger = logging.getLogger()


def main():
    mine_time = datetime.now()
    process = sys.argv[1]
    logger.info(f"Start process {process}")
    get_settings()
    logger.debug(settings)
    set_logger()
    if len(sys.argv) > 2:
        logger.error(f"Too many arguments")
        exit(1)
    elif len(sys.argv) < 2:
        logger.error(f"Executed process not specified")
        exit(1)

    logger.info(f"Process executed in {datetime.now() - mine_time} sec.")


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
    settings['ZM_ZABBIX_SENDER'] = os.getenv('ZM_ZABBIX_SENDER', "/usr/bin/zabbix_sender")
    # Zabbix agent configuration file
    settings['ZM_ZABBIX_SENDER_CONF'] = os.getenv('ZM_ZABBIX_SENDER_CONF', "/etc/zabbix/zabbix_agentd.conf")
    # OK value for Zabbix
    settings['ZM_ZABBIX_OK'] = os.getenv('ZABBIX_OK', 0)
    # Not OK value for Zabbix
    settings['ZM_ZABBIX_NOT_OK'] = os.getenv('ZM_ZABBIX_NOT_OK', 1)

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


if __name__ == '__main__':
    main()
