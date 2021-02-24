import json
from typing import Callable, Iterator, Generator
from tweetybird import TweetsDateInterval, Mentions


def extract_tweets(tweets: Iterator, retweet_origins: Mentions,
                   tweets_date_range: TweetsDateInterval) -> Generator:
    return (tweet for tweet in tweets if tweets_date_range(tweet) and retweet_origins(tweet))


if __name__ == '__main__':
    tweets_date_interval = TweetsDateInterval("2020-02-01")
    tweets_originators = Mentions("screen_name",
                                  ("ChineseWSJ", "FTChinese",
                                   "rijingzhongwen", "ChosunChinese",
                                   "bbcchinese", "dw_chinese"))
    with open('mod_tweet.js', 'r') as fp:
        with open('chinese_text_tweet.json', 'w', encoding='utf-8') as f_out:
            tweets = iter(json.load(fp))
            json.dump(list(extract_tweets(tweets, tweets_originators, tweets_date_interval)), f_out, indent=2,
                      ensure_ascii=False)
