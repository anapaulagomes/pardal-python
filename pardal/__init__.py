import logging
import os
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import sys


sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN', None),
    integrations=[sentry_logging]
)


def get_logger(name):
    log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        filename='pardal.log',
        filemode='a'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


def my_handler(type, value, tb):
    get_logger(__name__).exception(f'Uncaught exception: {value}')


sys.excepthook = my_handler
