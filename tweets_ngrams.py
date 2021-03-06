from collections import deque, Counter
from typing import List
from tweetybird import Tweet, tweet_text_minus_entities
from cjk_latin_emoji import RE_SEPARATORS, is_cjk
import json

"""
MDBG

https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=1&wdqb=c%3A阿尔茨海默症

https://dictionary.cambridge.org/dictionary/english-chinese-traditional/alzheimer-s?q=alzheimer%3Bs
"""


def hztweet_ngrams(tweet: Tweet, n) -> List[str]:
    ngrams = []
    q = deque([], maxlen=n)
    core_tweet = tweet_text_minus_entities(tweet)
    # Chinese-text tweets include punctuation marks; some tweets include English words
    for tweet_parts in RE_SEPARATORS.split(core_tweet):
        for codepoint in tweet_parts:
            if is_cjk(codepoint):
                # process only CJK code points
                q.append(codepoint)
                if len(q) == n:
                    ngrams.append(''.join(q))
                    q.popleft()

        q.clear()
    return ngrams


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
    with open('chinese_text_tweet.json', 'r') as fp:
        tweets = json.load(fp)
        for i, tweet in enumerate(tweets):
            print(f"{i}: {tweet['tweet']['full_text']}")
            ngrams_freq.add_ngrams(hztweet_ngrams(tweet, 7))

    print(ngrams_freq.ngrams_counter)


