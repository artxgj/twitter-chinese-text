from collections import deque
from collections.abc import Sequence, Generator, Mapping
from typing import List, Deque, Dict, Set
from twitter_objects import AbbreviatedTweet, next_tweet, is_tweet_in_sources, from_tweet_js_file
from general_helpers import dictlines_from_csv

import datetime
import re


RE_SEPARATORS = re.compile(r"[:?！？，。“”【】\"：…\n、（）～；•《》—「」·~丶]")

Zh_Tweets_Sources = {
    'ChineseWSJ',
    'ChosunChinese',
    'FTChinese',
    'KBSChinese',
    'asahi_shinsen',
    'bbcchinese',
    'dw_chinese',
    'nanyangpress',
    'rijingzhongwen',
    'zaobaosg',
    'CNS1952',
    'XinhuaChinese',
    'CEOBriefing',
    'AsiaFinance',
    'RFI_TradCn',
    'ParsTodayChina',
    'newsNZcn'
}


def valid_tweet_input_date(date_str: str):
    """
    raises an exception if the date_str value is not valid
    """
    datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return datetime.datetime.strptime(f"{date_str} 00:00:00 +0000", "%Y-%m-%d %H:%M:%S %z")


def is_cjk(c: str) -> bool:
    return 0x4E00 <= ord(c) <= 0x9FFF


class HZTweetNgram:
    def __init__(self, ngram: int):
        self._ngram = ngram
        self._deq: Deque[str] = deque([], maxlen=ngram)

    def extract(self, tweet: AbbreviatedTweet, include_hash_tags=True) -> List[str]:
        self._deq.clear()
        ngrams = []
        # Chinese-text tweets include punctuation marks; some tweets include English words
        for tweet_parts in RE_SEPARATORS.split(tweet.text_without_entities()):
            self._add_cjk_codepoints(tweet_parts, ngrams)

        if include_hash_tags:
            for hashtag in tweet.hashtags:
                self._add_cjk_codepoints(hashtag.text, ngrams)

        return ngrams

    def _add_cjk_codepoints(self, codepoints, ngrams):
        for codepoint in codepoints:
            if is_cjk(codepoint):
                # process only CJK code points
                self._deq.append(codepoint)
                if len(self._deq) == self._ngram:
                    ngrams.append(''.join(self._deq))
                    self._deq.popleft()
            else:
                self._deq.clear()  # not CJK codepoint, drop previously accumulated codepoints
        self._deq.clear()


class HanziTweetSummary:
    def __init__(self, tweet: AbbreviatedTweet):
        self.tweet_date = tweet.created_at
        self.tweet_id = tweet.id_int
        self.tweet_source = tweet.user_mentions[0].name
        self.tweet_text = tweet.full_text

    @staticmethod
    def field_names() -> Sequence[str]:
        return 'Date', 'Id', 'Source', 'Tweet'

    def to_dict(self, date_fmt: str = "%Y-%m-%d %H:%M:%S %Z", strip_newline: bool = True):
        return {
            'Date': self.tweet_date.strftime(date_fmt),
            'Id': self.tweet_id,
            'Source': self.tweet_source,
            'Tweet': self.tweet_text.replace('\n', '') if strip_newline else self.tweet_text
        }


def next_hanzi_tweet(tweet_js_filepath: str) -> AbbreviatedTweet:
    for tweet in next_tweet(from_tweet_js_file(tweet_js_filepath)):
        if is_tweet_in_sources(tweet, Zh_Tweets_Sources):
            yield tweet


def tweet_in_date_range(tweet: AbbreviatedTweet, start_date: datetime.datetime = None, end_date: datetime.datetime = None):
    """
    start_date and end_date must be both datetime objects, otherwise ignore date checks
    """
    return False if isinstance(start_date, datetime.datetime) and isinstance(end_date, datetime.datetime) and \
                    (tweet.created_at < start_date or tweet.created_at > end_date) else True


def next_hanzi_tweet_summarized(tweet_js_filepath: str) -> Generator[HanziTweetSummary, None, None]:
    """
    Generates summarized Chinese-text tweet
    :param tweet_js_filepath: path of Twitter-archive's filepath (tweet.js)
    :return: Generator[HanziTweetSummary, None, None]
    """
    for tweet in next_hanzi_tweet(tweet_js_filepath):
        yield HanziTweetSummary(tweet)


def next_HanziTweetSummary(summarized_tweets_csv_filepath: str) -> Generator[Mapping, None, None]:
    """

    :param summarized_tweets_csv_filepath:
    :return: a Mapping with keys 'Date', 'Id', 'Source', 'Tweet'
    """
    return dictlines_from_csv(summarized_tweets_csv_filepath, None)


def next_vocab_tweets_index(vocab_tweets_index_csv_filepath: str) -> Generator[Mapping, None, None]:
    """
    :param vocab_tweets_index_csv_filepath:
    :return: a Mapping with keys "Word", "Tweet_Ids"
    """
    return dictlines_from_csv(vocab_tweets_index_csv_filepath, None)


def next_tweets_vocab_index(tweets_vocab_index_csv_filepath: str) -> Generator[Mapping, None, None]:
    """
    :param tweets_vocab_index_csv_filepath:
    :return: a Mapping with keys "Tweet_Id", "Words"
    """
    return dictlines_from_csv(tweets_vocab_index_csv_filepath, None)


def cache_tweets_summary_csv(filepath: str) -> Dict[str, Dict]:
    cache = dict()

    for row in next_HanziTweetSummary(filepath):
        cache[row['Id']] = {
            'Date': row['Date'],
            'Source': row['Source'],
            'Tweet': row['Tweet']
        }

    return cache


def cache_words_tweetids_csv(filepath: str) -> Dict[str, List[str]]:
    return {row['Word']: row['Tweet_Ids'].split(',') for row in next_vocab_tweets_index(filepath)}


def cache_tweetid_words_csv(filepath: str) -> Dict[str, Set[str]]:
    return {row['Tweet_Id']: set(row['Words'].split(',')) for row in next_tweets_vocab_index(filepath)}
