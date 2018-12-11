from pardal import get_logger
from pardal.authserver import run_authentication_flow
from pardal.authserver.app import initialize_db
from pardal.buffers import HomeTimeline
from pardal.speaking import say


logger = get_logger(__name__)


def start_app(api):
    logger.info('Retrieving timeline from Twitter')
    say('Retrieving timeline from Twitter.')

    timeline = HomeTimeline(api)
    timeline.listen()


initialize_db()

api = run_authentication_flow()

if api:
    start_app(api)
