from abc import ABC, abstractmethod

from pardal import get_logger
from pardal.api.exceptions import InvalidOrExpiredToken
from pardal.authserver.app import API_ADDRESS
from pardal.authserver.app import AuthToken

logger = get_logger(__name__)


class APIWrapper(ABC):
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.callback_url = f'{API_ADDRESS}/callback'
        self.request_token_url = 'https://api.twitter.com/oauth/request_token'
        self.authorization_url = 'https://api.twitter.com/oauth/authorize'
        self.access_token_url = 'https://api.twitter.com/oauth/access_token'
        self.api_base_url = 'https://api.twitter.com/1.1'
        self._api = None
        self._headers = None

    @abstractmethod
    def get_authentication_tokens(self):
        raise NotImplementedError

    @abstractmethod
    def get_authorized_tokens(self, request_tokens, oauth_verifier):
        raise NotImplementedError

    @abstractmethod
    def verify_credentials(self):
        raise NotImplementedError

    @abstractmethod
    def get_home_timeline(self):
        raise NotImplementedError

    @abstractmethod
    def when_rate_limit_reset(self):
        raise NotImplementedError

    def has_token(self):
        return AuthToken.select().exists()

    def is_token_valid(self):
        """Check if token exists and if it is valid."""
        if AuthToken.select().exists():
            try:
                self.verify_credentials()
                return True
            except InvalidOrExpiredToken:
                logger.exception('Invalid or Expired Token')
                AuthToken.select().order_by(
                    AuthToken.id.desc()).first().delete_instance()
                self._api = None
        return False
