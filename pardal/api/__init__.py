import os

from pardal import get_logger

__all__ = ('api',)
logger = get_logger(__name__)


def get_twitter_api():
    is_testing = os.getenv('FAKE_TWITTER_API', 'True')
    consumer_key = os.getenv('CONSUMER_KEY', 'xxx')
    consumer_secret = os.getenv('CONSUMER_SECRET', 'yyy')

    if is_testing in ['1', 'true', 'True']:
        from pardal.api.fake import FakeTwitterAPI as TwitterAPI
        logger.info('Using: FakeTwitterAPI')
    else:
        from pardal.api.live import LiveTwitterAPI as TwitterAPI
        logger.info('Using: LiveTwitterAPI')

    return TwitterAPI(consumer_key, consumer_secret)


api = get_twitter_api()
