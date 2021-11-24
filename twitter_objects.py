from collections.abc import Mapping, Set, Sequence
from typing import Dict, Optional, List, Generator

import datetime
import json
import re

"""
Reference:
https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
"""

_TWEET_V1_DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"


class Indices:
    def __init__(self, indices: Sequence):
        self.begin, self.end = indices

        if isinstance(self.begin, str):
            self.begin = int(self.begin)

        if isinstance(self.end, str):
            self.end = int(self.end)


class Hashtag:
    def __init__(self, ht: Mapping):
        self.text = ht["text"]
        self.indices: Indices = Indices(ht["indices"])


class UserMention:
    def __init__(self, um: Mapping):
        self.name = um["name"]
        self.screen_name = um["screen_name"]
        self.indices: Indices = Indices(um["indices"])
        self.id_str = um["id_str"]
        self.id_int = int(um["id"])


class EntityUrl:
    def __init__(self, ent_url: Mapping):
        # url: Wrapped URL, corresponding to the value embedded directly into the raw Tweet text, and the values for the
        # indices parameter.
        self.url: str = ent_url["url"]
        self.display_url: str = ent_url.get("display_url", None)
        self.expanded_url: str = ent_url.get("expanded_url", None)
        self.indices: Indices = Indices(ent_url["indices"])


class Cashtag:
    def __init__(self, cashtag: Mapping):
        # first integer of indices represents the location of the $ character
        self.indices: Indices = Indices(cashtag["indices"])
        self.text = cashtag["text"]


class Size:
    def __init__(self, size: Mapping):
        self.h, self.w, self.resize = size['h'], size['w'], size['resize']

        if isinstance(self.h, str):
            self.h = int(self.h)

        if isinstance(self.w, str):
            self.w = int(self.w)


class MediaSize:
    def __init__(self, name: str, size: Mapping):
        self.name: str = name
        self.size = Size(size)

    @property
    def h(self) -> int:
        return self.size['h']

    @property
    def w(self) -> int:
        return self.size['w']

    @property
    def resize(self) -> str:
        return self.size['resize']


class Medium:
    def __init__(self, medium: Mapping):
        self.expanded_url = medium["expanded_url"]
        self.source_status_id: Optional[int] = medium.get("source_status_id")
        self.indices: Indices = Indices(medium["indices"])
        self.url = medium["url"]
        self.media_url = medium["media_url"]
        self.id_str = medium["id_str"]
        self.source_user_id: Optional[int] = medium.get("source_user_id", None)
        self.id = int(medium["id"])
        self.media_url_https = medium['media_url_https']
        self.sizes = [MediaSize(name, size) for name, size in medium['sizes'].items()]
        self.type = medium['type']
        self.display_url = medium['display_url']


class AbbreviatedTweet:
    def __init__(self, tweet: Mapping):
        self.id_int = int(tweet["id"])
        self.source: Optional[str] = tweet.get("source", None)
        self.full_text: str = tweet['full_text']
        self.display_text_range: Indices = Indices(tweet['display_text_range'])
        self.lang: Optional[str] = tweet.get('lang', None)
        self.truncated: bool = tweet['truncated']
        self.created_at: datetime.datetime = datetime.datetime.strptime(tweet['created_at'], _TWEET_V1_DATE_FORMAT)
        self.user_mentions: List[UserMention] = [UserMention(um) for um in tweet['entities']['user_mentions']]
        self.hashtags: List[Hashtag] = [Hashtag(ht) for ht in tweet['entities']['hashtags']]
        self.symbols: List[Cashtag] = [Cashtag(ct) for ct in tweet['entities']['symbols']]
        self.entity_urls: List[EntityUrl] = [EntityUrl(url) for url in tweet['entities']['urls']]
        self.media: List[Medium] = [Medium(medium) for medium in tweet['entities'].get('media', [])]

    def text_without_entities(self, skip_rt: bool = True) -> str:
        # initialize with display_text_range's indices, which covers the entire display text
        # Two indices entries:
        #   (display_text_range.begin, display_text_range.begin) as the first entry,
        #   (display_text_range.end, display_text_range.end) as the last entry
        # The display_text includes entities like hash tags, user mentions, symbols, etc. Each entity
        # has indices. The indices do not overlap.
        entity_indices = [Indices([self.display_text_range.begin, self.display_text_range.begin]),
                          Indices([self.display_text_range.end, self.display_text_range.end])]

        for entity_collection in (self.user_mentions, self.hashtags, self.symbols, self.entity_urls, self.media):
            for entity in entity_collection:
                entity_indices.append(entity.indices)

        entity_indices.sort(key=lambda ix: ix.begin)

        text_buffer = []
        for i in range(0, len(entity_indices)-1):
            text_buffer.append(self.full_text[entity_indices[i].end: entity_indices[i+1].begin])

        text_minus_entities = ''.join(text_buffer)
        return text_minus_entities[3:] if skip_rt and text_minus_entities[:3] == 'RT ' else text_minus_entities


TweetData = Dict[str, Dict]


class IncorrectTweetJsFile(Exception):
    pass


# to do later, create a file object with context manager to read tweet_js_file

def from_tweet_js_file(filepath: str) -> List[TweetData]:
    with open(filepath, 'r') as fp:
        js = fp.readlines()

        if re.match(r'^window\.YTD\.tweet\.part\d+ =', js[0]):
            js[0] = js[0].split('=')[1].strip()
            tweets = json.loads(''.join(js))
            return tweets
        else:
            raise IncorrectTweetJsFile(f"{filepath} is not a tweet js file.")


def next_tweet(tweet_data: Sequence[TweetData]) -> Generator[AbbreviatedTweet, None, None]:
    for elem in tweet_data:
        yield AbbreviatedTweet(elem['tweet'])


def is_tweet_in_sources(tweet: AbbreviatedTweet, sources: Set[str]) -> bool:
    for user_mention in tweet.user_mentions:
        if user_mention.screen_name in sources:
            return True

    return False
