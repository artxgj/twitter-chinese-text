import datetime
from zoneinfo import ZoneInfo
from typing import Optional, Dict, Iterable, List

TWITTER_DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"


"""
https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
"""

def is_retweeted_text(tweet_json: Dict[str, Dict]) -> bool:
    return tweet_json['tweet'].get('full_text', '')[:4] == 'RT @'


class TweetsDateInterval:
    def __init__(self, start_date: str, end_date: Optional[str] = None, timezone=ZoneInfo("UTC")):
        self._start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").astimezone(timezone)

        if end_date is None:
            self._end_date = datetime.datetime.today().astimezone(timezone)
        else:
            self._end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").astimezone(timezone)

        assert self._start_date < self._end_date

    def __call__(self, *args, **kwargs):
        tweet_json, *the_rest = args
        tweet: Dict = tweet_json['tweet']
        tweet_date = datetime.datetime.strptime(tweet['created_at'], TWITTER_DATE_FORMAT)
        return tweet_date in self

    def __contains__(self, item: datetime.datetime):
        return self._start_date <= item <= self._end_date


class Mentions:
    def __init__(self, user_mentions_attribute: str, names: Iterable[str]):
        self._mentions_tag = user_mentions_attribute
        self._users_names = set(names)

    def __call__(self, *args, **kwargs):
        tweet_json, *the_rest = args
        user_mentions: List[Dict] = tweet_json['tweet']['entities']['user_mentions']
        return any(user_mention[self._mentions_tag] in self for user_mention in user_mentions)

    def __contains__(self, item):
        return item in self._users_names


def tweet_hashtags_text(tweet: Dict[str, Dict]) -> List[str]:
    return [htag["text"] for htag in tweet['tweet']["entities"]["hashtags"]]


def tweet_symbols_text(tweet: Dict[str, Dict]) -> List[str]:
    return [symbol["text"] for symbol in tweet['tweet']["entities"]["symbols"]]


def tweet_urls(tweet: Dict[str, Dict]) -> List[str]:
    return [url["url"] for url in tweet['tweet']["entities"]["urls"]]


def tweet_full_text(tweet: Dict[str, Dict]) -> str:
    return tweet['tweet']['full_text']


def tweet_text_minus_entities(tweet: Dict[str, Dict]) -> str:
    tweet_tree = tweet['tweet']
    text_start, text_end = tweet_tree["display_text_range"]
    indices = [entity['indices'] for entity_type in ("hashtags", "symbols", "user_mentions", "urls")
               for entity in tweet_tree["entities"][entity_type]]

    flat_indices = sorted([int(text_start)] + [int(item) for pair in indices for item in pair] + [int(text_end)])
    full_text = tweet_full_text(tweet)
    return ''.join(full_text[flat_indices[i]:flat_indices[i+1]] for i in range(0, len(flat_indices), 2))

