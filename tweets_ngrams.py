from collections import deque, Counter
from typing import List, Deque
from hashtags import extract_hashtags
from tweetybird import TweetDict, tweet_text_minus_entities
from cjk_latin_emoji import RE_SEPARATORS, is_cjk
import json

"""
MDBG

https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=1&wdqb=豐田
https://dictionary.cambridge.org/dictionary/english-chinese-traditional/alzheimer-s?q=alzheimer%3Bs

https://translate.google.com/?sl=auto&tl=zh-TW&text=RT%20%40ChineseWSJ%3A%20全球最大的香槟酒生产商LVMH已经收购了Armand%20de%20Brignac%2050%25的股份，该品牌是说唱歌手Jay-Z旗下的高端香槟品牌%E3%80%82这一品牌是著名气泡酒产区最年轻的品牌之一，以其每瓶售价数百美元的金属酒瓶而闻名%E3%80%82https%3A%2F%2Ft.co%2FwJ…&op=translate

https://translate.google.com/?sl=auto&tl=en&text=RT%20%40ChineseWSJ%3A%20全球最大的香槟酒生产商LVMH已经收购了Armand%20de%20Brignac%2050%25的股份，该品牌是说唱歌手Jay-Z旗下的高端香槟品牌%E3%80%82这一品牌是著名气泡酒产区最年轻的品牌之一，以其每瓶售价数百美元的金属酒瓶而闻名%E3%80%82https%3A%2F%2Ft.co%2FwJ…&op=translate
"""


class HZTweetNgram:
    def __init__(self, ngram: int):
        self._ngram = ngram
        self._deq: Deque[str] = deque([], maxlen=ngram)

    def extract(self, tweet: TweetDict, include_hash_tags=True) -> List[str]:
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
    tweet_ngrams = HZTweetNgram(3)

    with open('chinese_text_tweet.json', 'r') as fp:
        tweets = json.load(fp)
        for i, tweet in enumerate(tweets):
            print(f"{i}: {tweet['tweet']['full_text']}")
            ngrams_freq.add_ngrams(tweet_ngrams.extract(tweet))

    print(ngrams_freq.ngrams_counter)


