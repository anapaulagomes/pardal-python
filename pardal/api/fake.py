from pardal.api.base import APIWrapper
from pardal.authserver.app import API_ADDRESS
from pardal.authserver.app import AuthToken
import json


class FakeTwitterAPI(APIWrapper):
    def get_authentication_tokens(self):
        args = 'callback?oauth_token=aaa&oauth_verifier=ooo'
        auth_url = f'{API_ADDRESS}/{args}'
        auth = {
            'oauth_token': 'zzz',
            'oauth_token_secret': 'yyy',
            'auth_url': auth_url
        }
        return auth

    def get_authorized_tokens(self, oauth_verifier, request_tokens=[]):
        AuthToken.get_or_create(
            username='theSeanCook',
            defaults={
                'oauth_token': 'saved-access-token',
                'oauth_token_secret': 'saved-access-token-secret',
            }
        )

        return {
            'oauth_token': 'bbb',
            'oauth_token_secret': 'ccc',
            'screen_name': 'theSeanCook',
            'user_id': '00000000',
        }

    def verify_credentials(self):
        fixture_file = open('tests/fixtures/credentials.json')
        return json.load(fixture_file)

    def get_home_timeline(self):
        fixture_file = open('tests/fixtures/timeline.json')
        return json.load(fixture_file)

    def when_rate_limit_reset(self):
        return 10
