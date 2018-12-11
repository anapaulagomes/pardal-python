from flask import abort, session, request, redirect

from pardal.api.exceptions import InvalidOrExpiredToken
from pardal.authserver.app import app
from pardal.api import api
from pardal import get_logger


logger = get_logger(__name__)


@app.route('/')
def index():
    return 'It works!'


@app.route('/authorize')
def oauth_authorize():
    logger.info('Accessing authorize endpoint')
    auth = api.get_authentication_tokens()
    session['request_token'] = [
        auth['oauth_token'], auth['oauth_token_secret']]
    return redirect(auth['auth_url'])


@app.route('/callback')
def oauth_callback():
    logger.info('Accessing callback endpoint')
    oauth_verifier = request.args.get('oauth_verifier')
    request_token = session.pop('request_token', None)

    api.get_authorized_tokens(oauth_verifier, request_token)

    try:
        api.verify_credentials()
    except InvalidOrExpiredToken:
        logger.exception('Verify credentials failed')
        abort(401)
    return ''
