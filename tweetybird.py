import datetime
from zoneinfo import ZoneInfo
from typing import Optional, Dict, Iterable, List

TWITTER_DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"


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
