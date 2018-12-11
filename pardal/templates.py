import re


"""
Format the tweets using some pre-defined template.
In the future the user should be able to configure their
own templates.
"""
SOURCE_PATTERN = re.compile(r'<a.*>(.*)<\/a>')


def _parse_source(tweet_source):
    source = re.search(SOURCE_PATTERN, tweet_source)
    if source:
        return source.group(1)
    return tweet_source


def tweet(raw_tweet):
    source = _parse_source(raw_tweet['source'])
    formatted = f"{raw_tweet['user']['screen_name']} : " \
                f"{raw_tweet['full_text']}. " \
                f"{raw_tweet['created_at']} via {source}"

    return formatted
