from pardal import get_logger
from pardal.api.base import APIWrapper
from pardal.api.exceptions import InvalidOrExpiredToken
from pardal.authserver.app import AuthToken
import time
from requests_oauthlib import OAuth1Session


logger = get_logger(__name__)


class LiveTwitterAPI(APIWrapper):
    def _request(self, url):
        error_codes = {
            89: {
                'message': 'Invalid or expired token',
                'exception': InvalidOrExpiredToken
            }
        }
        response = self.api.get(f'{url}?tweet_mode=extended')
        self._headers = response.headers
        json_response = response.json()

        if isinstance(json_response, dict):
            if 'errors' in json_response.keys():
                error_code = error_codes.get(
                    json_response['errors'][0]['code'])
                if error_code:
                    raise error_code['exception']
                else:
                    logger.error('unknown error: ', json_response)
                    raise Exception('unknown error: ', json_response)

        return json_response

    @property
    def api(self):
        if self._api:
            return self._api

        token = AuthToken.select().order_by(AuthToken.id.desc()).first()

        self._api = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=token.oauth_token,
            resource_owner_secret=token.oauth_token_secret)
        return self._api

    def get_authentication_tokens(self):
        oauth = OAuth1Session(
            self.consumer_key, client_secret=self.consumer_secret)
        request_token = oauth.fetch_request_token(self.request_token_url)
        authorization_url = oauth.authorization_url(self.authorization_url)
        request_token['auth_url'] = authorization_url
        return request_token

    def get_authorized_tokens(self, oauth_verifier, request_token):
        self._api = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=request_token[0],
            resource_owner_secret=request_token[1],
            verifier=oauth_verifier
        )

        oauth_tokens = self._api.fetch_access_token(self.access_token_url)
        oauth_token = oauth_tokens.get('oauth_token')
        oauth_token_secret = oauth_tokens.get('oauth_token_secret')

        AuthToken.get_or_create(
            username=oauth_tokens['screen_name'],
            defaults={
                'oauth_token': oauth_token,
                'oauth_token_secret': oauth_token_secret
            }
        )
        return self._api

    def verify_credentials(self):
        url = f'{self.api_base_url}/account/verify_credentials.json'
        return self._request(url)

    def get_home_timeline(self):
        url = f'{self.api_base_url}/statuses/home_timeline.json'
        return self._request(url)

    def when_rate_limit_reset(self):
        """
        Get remaining rate limit window and
        calculates how many seconds are left.
        """
        if self._headers is None:
            self.verify_credentials()

        left = self._headers.get('x-rate-limit-reset')
        if left:
            return (left - time.time()) % 60
        return None
