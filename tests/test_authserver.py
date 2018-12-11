import flask

from pardal.api.exceptions import InvalidOrExpiredToken
from pardal.authserver import (
    is_server_running, run_authorization_flow, start_server,
    run_authentication_flow
)
from pardal.authserver.app import AuthToken
import pytest
import sys
from unittest.mock import patch, call
import urllib.error


class TestApi:
    def test_ask_user_authorization(self, client):
        response = client.get('/authorize')

        assert response.status_code == 302
        assert flask.session['request_token'] == ['zzz', 'yyy']

    def test_receive_token_and_verifier_on_callback(self, client):
        with client.session_transaction() as session:
            session['request_token'] = ['zzz', 'yyy']
        args = {'oauth_token': 'aaa', 'oauth_verifier': 'ooo'}
        response = client.get('/callback', query_string=args)

        assert response.status_code == 200

    @patch('pardal.authserver.endpoints.api.verify_credentials')
    def test_handle_with_expired_token(self, mock_api, client):
        with client.session_transaction() as session:
            session['request_token'] = ['zzz', 'yyy']
        args = {'oauth_token': 'aaa', 'oauth_verifier': 'ooo'}
        mock_api.side_effect = InvalidOrExpiredToken()

        response = client.get('/callback', query_string=args)

        assert response.status_code == 401


class TestFlow:
    def test_return_true_if_is_running(self):
        with patch('pardal.authserver.urllib.request.urlopen'):
            assert is_server_running() is True

    def test_return_false_if_server_is_not_running(self):
        with patch('pardal.authserver.urllib.request.urlopen') as mock_url:
            mock_url.side_effect = urllib.error.URLError('Connection refused')

            assert is_server_running() is False

    @pytest.mark.skipif(
        sys.platform.startswith('win'),
        reason='valid only for MacOS or Linux'
    )
    def test_start_server_linux_or_osx(self):
        with patch('pardal.authserver.subprocess.Popen') as mock_popen, \
                patch('pardal.authserver.urllib.request.urlopen') as mock_url:
            mock_url.side_effect = urllib.error.URLError('Connection refused')

            start_server()

        assert mock_popen.called
        assert mock_popen.call_args(['sh', 'bin/server.sh'])

    @pytest.mark.skipif(
        sys.platform == 'darwin' or sys.platform == 'linux',
        reason='valid only for Windows'
    )
    def test_start_server_windows(self):
        with patch('pardal.authserver.subprocess.Popen') as mock_popen, \
                patch('pardal.authserver.urllib.request.urlopen') as mock_url:
            mock_url.side_effect = urllib.error.URLError('Connection refused')

            start_server()

        assert mock_popen.called
        assert mock_popen.call_args(['bin\\server.bat'])

    def test_start_server_only_if_not_running(self):
        with patch('pardal.authserver.urllib.request.urlopen') as mock_url, \
                patch('pardal.authserver.subprocess.Popen') as mock_popen:
            mock_url.side_effect = urllib.error.URLError('Connection refused')

            assert is_server_running() is False

            start_server()

            assert mock_popen.called

    def test_do_not_start_server_if_running(self):
        with patch('pardal.authserver.urllib.request.urlopen'), \
                patch('pardal.authserver.subprocess.Popen') as mock_popen:

            assert is_server_running() is True

            start_server()

            assert mock_popen.called is False

    @patch('pardal.authserver.say')
    def test_open_url_to_user(self, mock_say):
        msg = 'Please wait while an access token is retrieved from Twitter.'
        with patch('pardal.authserver.start_server') as mock_start_server, \
                patch('pardal.authserver.webbrowser.open') as mock_browser:
            run_authorization_flow()

            assert mock_start_server.called
            assert mock_say.call_args(msg)
            assert mock_browser.called

    def test_return_api_if_token_is_valid(self):
        AuthToken.create(
            username='pineapples',
            oauth_token='saved-access-token',
            oauth_token_secret='saved-access-token-secret',
        )
        api = run_authentication_flow()

        assert api is not None

    @patch('pardal.authserver.say')
    @patch('pardal.authserver.time.sleep')
    @patch('pardal.authserver.webbrowser.open')
    def test_return_none_if_token_exists_but_invalid(
            self, mock_browser, mock_sleep, mock_say):
        AuthToken.create(
            username='pineapples',
            oauth_token='saved-access-token',
            oauth_token_secret='saved-access-token-secret',
        )
        with patch('pardal.api.fake.FakeTwitterAPI.verify_credentials') \
                as mock_api:
            mock_api.side_effect = InvalidOrExpiredToken
            api = run_authentication_flow()

        assert api is None

    @patch('pardal.authserver.say')
    @patch('pardal.authserver.time.sleep')
    @patch('pardal.authserver.webbrowser.open')
    @patch('pardal.authserver.subprocess.Popen')
    def test_return_none_if_token_does_not_exists_and_user_do_not_authorize(
            self, mock_server, mock_browser, mock_sleep, mock_say):
        AuthToken.delete().execute()
        expected_say = [
            call(
                'Please wait while an access token is retrieved from Twitter.'
            ),
            call('Waiting for the access token.'),
            call('Waiting for the access token.'),
            call('Waiting for the access token.'),
            call('Authentication failed.')
        ]

        api = run_authentication_flow()

        assert api is None
        assert mock_browser.called is True
        assert mock_sleep.call_count == 3  # max number of attempts reached
        assert mock_say.call_args_list == expected_say

    @patch('pardal.authserver.say')
    @patch('pardal.authserver.time.sleep')
    @patch('pardal.authserver.webbrowser.open')
    def test_return_api_if_token_does_not_exists_but_user_authorize(
            self, mock_browser, mock_user, mock_say):
        AuthToken.delete().execute()

        def create_token(x):
            return AuthToken.create(
                username='pineapples',
                oauth_token='saved-access-token',
                oauth_token_secret='saved-access-token-secret',
            )
        # dirty mock to simulate the user authenticating
        mock_user.side_effect = create_token

        api = run_authentication_flow()

        assert api is not None
