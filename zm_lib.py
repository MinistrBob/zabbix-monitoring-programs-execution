import logging
import sys
from urllib import request, parse

from pyzabbix import ZabbixMetric, ZabbixSender


class Settings(object):
    """
    Program settings like class
    """

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)

    def __str__(self):
        return str(self.__dict__)


def get_logger(settings):
    logger = logging.getLogger()
    # Log to stdout
    if settings.ZM_DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    stdout_log_formatter = logging.Formatter('%(asctime)s|%(levelname)-5s|%(funcName)-22s| %(message)s')
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(stdout_log_formatter)
    logger.addHandler(stdout_handler)
    return logger


def raise_error(settings, logger, message, do_error_exit=True):
    logger.error(f"<b>ERROR</b>: {message}")
    telegram_message = f"""❌ <b>zm.py</b> from <b>{settings.HOSTNAME}</b>
<code>{message}</code>
"""
    telegram_notification(settings, logger, telegram_message)
    if do_error_exit:
        exit(1)


def telegram_notification(settings, logger, message):
    if settings.ZM_TELEGRAM_NOTIF:
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'
        # }
        logger.debug(f"message={message}")
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


def zabbix_sender(settings, logger, data):
    metrics = []
    for metric in data:
        m = ZabbixMetric(settings.ZM_ZABBIX_HOST_NAME, metric, data[metric])
        metrics.append(m)
    zbx = ZabbixSender(settings.ZM_ZABBIX_IP)
    logger.info(f"Send metrics")
    zbx.send(metrics)


def main():
    pass


if __name__ == '__main__':
    main()
