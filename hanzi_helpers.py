from collections import deque
from typing import List, Deque
from twitter_objects import AbbreviatedTweet, next_tweet, is_tweet_in_sources, from_tweet_js_file
import re


RE_SEPARATORS = re.compile(r"[:?！？，。“”【】\"：…\n、（）～；•《》—「」·~]")

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
    'zaobaosg'
}


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
        self._deq.clear()


def next_hanzi_tweet(tweet_js_filepath: str):
    for tweet in next_tweet(from_tweet_js_file(tweet_js_filepath)):
        if is_tweet_in_sources(tweet, Zh_Tweets_Sources):
            yield tweet
