from pardal import get_logger
from pardal.api import api
from pardal.authserver.app import API_ADDRESS
from pardal.speaking import say
import subprocess
import time
import urllib.request
import urllib.error
import webbrowser

logger = get_logger(__name__)


def is_server_running():
    try:
        urllib.request.urlopen(f'http://{API_ADDRESS}')
    except urllib.error.URLError:
        return False
    logger.warning('Server is running already')
    return True


def start_server():
    logger.info('Starting server...')

    if is_server_running():
        return

    subprocess.Popen(['flask', 'run'])


def run_authorization_flow():
    """Run authorization flow where the user must
    authorize Pardal to access their Twitter account."""
    start_server()

    logger.info('Starting not logged user flow...')
    say('Please wait while an access token is retrieved from Twitter.')

    # FIXME if Linux copy the address to user clipboard
    webbrowser.open(f'{API_ADDRESS}/authorize')


def run_authentication_flow():
    """Manage the authentication flow for logged and not logged users."""
    if api.is_token_valid():
        return api
    else:
        run_authorization_flow()

        attempts = 0
        max_attempts = 3
        while not api.is_token_valid() and attempts < max_attempts:
            say('Waiting for the access token.')
            time.sleep(10)
            attempts += 1
        if attempts == max_attempts:
            logger.error('Authentication failed.')
            say('Authentication failed.')
        elif api.is_token_valid():
            return api
        return
