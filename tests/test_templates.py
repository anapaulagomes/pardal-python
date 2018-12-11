import json

import pytest

from pardal import templates


@pytest.mark.parametrize('tweet_source,expected_source', [
    (
            '<a href="http://twitter.com/download/android" rel="nofollow">'
            'Twitter for Android</a>',
            'Twitter for Android'
    ),
    (
            '<a href="http://folha.com" rel="nofollow">'
            'Folha com welcome-app 1.0</a>',
            'Folha com welcome-app 1.0'
    ),
    (
            '<a href="https://www.echobox.com" rel="nofollow">'
            'Echobox Social</a>',
            'Echobox Social'
    )
])
def test_parse_source(tweet_source, expected_source):
    assert templates._parse_source(tweet_source) == expected_source


def test_tweet_template():
    tweets = json.load(open('tests/fixtures/timeline.json'))
    raw_tweet = tweets[0]
    formatted_tweet = templates.tweet(raw_tweet)
    expected_formatted_tweet = 'oauth_dancer : just another test. ' \
                               'Tue Aug 28 21:16:23 +0000 2012 ' \
                               'via OAuth Dancer Reborn'

    assert formatted_tweet == expected_formatted_tweet
