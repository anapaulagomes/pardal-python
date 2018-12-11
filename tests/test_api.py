from unittest.mock import patch

from pardal.api import api
from pardal.api.exceptions import InvalidOrExpiredToken
from pardal.authserver.app import API_ADDRESS
from pardal.authserver.app import AuthToken


def test_get_authentication_tokens():
    auth = api.get_authentication_tokens()

    args = 'callback?oauth_token=aaa&oauth_verifier=ooo'
    auth_url = f'{API_ADDRESS}/{args}'
    expected_tokens = {
        'oauth_token': 'zzz',
        'oauth_token_secret': 'yyy',
        'auth_url': auth_url
    }

    assert auth == expected_tokens


def test_get_authorized_tokens(db):
    request_tokens = ['zzz', 'ddd']
    oauth_verifier = 'ooo'
    tokens = api.get_authorized_tokens(
        oauth_verifier, request_tokens=request_tokens)

    assert tokens['oauth_token'] == 'bbb'
    assert tokens['oauth_token_secret'] == 'ccc'


def test_verify_credentials():
    credentials = api.verify_credentials()

    assert credentials['screen_name'] == 'theSeanCook'


def test_timeline():
    credentials = api.get_home_timeline()

    assert credentials[0]['full_text'] == 'just another test'


def test_save_tokens_on_db():
    request_tokens = ['zzz', 'ddd']
    oauth_verifier = 'ooo'

    api.get_authentication_tokens()
    api.get_authorized_tokens(oauth_verifier, request_tokens=request_tokens)

    assert AuthToken.select().count() == 1


def test_return_time_left_from_rate_limit_reset():
    when = api.when_rate_limit_reset()

    assert when == 10


def test_match_methods_from_fake_and_live_api():
    from pardal.api.base import APIWrapper
    from pardal.api.fake import FakeTwitterAPI
    from pardal.api.live import LiveTwitterAPI

    for method in APIWrapper.__abstractmethods__:
        assert method in LiveTwitterAPI.__dict__.keys()
        assert method in FakeTwitterAPI.__dict__.keys()


def test_return_true_if_credentials_is_valid():
    assert api.is_token_valid() is True


def test_delete_token_and_speak_error_message_if_token_invalid():
    AuthToken.create(
        username='pineapples',
        oauth_token='saved-access-token',
        oauth_token_secret='saved-access-token-secret',
    )

    with patch('pardal.api.fake.FakeTwitterAPI.verify_credentials') \
            as mock_api:
        mock_api.side_effect = InvalidOrExpiredToken
        assert api.is_token_valid() is False

    assert AuthToken.select().where(
        AuthToken.username == 'pineapples').count() == 0


def test_return_false_if_token_does_not_exists():
    AuthToken.delete().execute()

    assert api.is_token_valid() is False


def test_has_token():
    AuthToken.create(
        username='pineapples',
        oauth_token='saved-access-token',
        oauth_token_secret='saved-access-token-secret',
    )

    assert api.has_token() is True


def test_does_not_have_token():
    AuthToken.delete().execute()

    assert api.has_token() is False
