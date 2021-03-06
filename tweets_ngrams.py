from collections import deque, Counter
from typing import List, Deque
from hashtags import extract_hashtags
from tweetybird import Tweet, tweet_text_minus_entities
from cjk_latin_emoji import RE_SEPARATORS, is_cjk
import json

"""
MDBG

https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=1&wdqb=c%3A阿尔茨海默症

https://dictionary.cambridge.org/dictionary/english-chinese-traditional/alzheimer-s?q=alzheimer%3Bs
"""


class HZTweetNgram:
    def __init__(self, ngram: int):
        self._ngram = ngram
        self._deq: Deque[str] = deque([], maxlen=ngram)

    def extract(self, tweet: Tweet, include_hash_tags=True) -> List[str]:
        self._deq.clear()
        ngrams = []
        core_tweet = tweet_text_minus_entities(tweet)
        # Chinese-text tweets include punctuation marks; some tweets include English words
        for tweet_parts in RE_SEPARATORS.split(core_tweet):
            self._add_cjk_codepoints(tweet_parts, ngrams)

        if include_hash_tags:
            for hashtag in extract_hashtags(tweet):
                self._add_cjk_codepoints(hashtag, ngrams)

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


if __name__ == '__main__':
    ngrams_freq = NGramsCounter()
    tweet_ngrams = HZTweetNgram(5)

    with open('chinese_text_tweet.json', 'r') as fp:
        tweets = json.load(fp)
        for i, tweet in enumerate(tweets):
            print(f"{i}: {tweet['tweet']['full_text']}")
            ngrams_freq.add_ngrams(tweet_ngrams.extract(tweet))

    print(ngrams_freq.ngrams_counter)


