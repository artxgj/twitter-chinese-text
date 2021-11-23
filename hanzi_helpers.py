from collections import deque, Counter
from typing import List, Deque
from twitter_objects import AbbreviatedTweet, is_tweet_in_sources
import re
import string


RE_SEPARATORS = re.compile(r"[:?！？，。“”【】\"：…\n、（）～；•《》—「」·~]")

_LETTER_DIGITS = set(string.digits + string.ascii_letters)


def is_cjk(c: str) -> bool:
    return 0x4E00 <= ord(c) <= 0x9FFF


def is_letter_digit(c: str) -> bool:
    return c in _LETTER_DIGITS


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


class NGramsCounter:
    def __init__(self):
        self._counter = Counter()

    def add_ngrams(self, ngrams: List[str]):
        for ngram in ngrams:
            self.add_ngram(ngram)

    def add_ngram(self, ngram: str):
        self._counter[ngram] += 1

    @property
    def ngrams_counter(self):
        return self._counter
