import json
from typing import Iterator, Generator
from tweetybird import from_tweet_js_file, TweetsDateInterval, Mentions, is_zh_tweet


def extract_tweets(tweets: Iterator, retweet_origins: Mentions,
                   tweets_date_range: TweetsDateInterval) -> Generator:
    return (tweet for tweet in tweets if tweets_date_range(tweet) and retweet_origins(tweet))


if __name__ == '__main__':
    tweets_date_interval = TweetsDateInterval("2020-02-01")
    with open('chinese_text_tweet.json', 'w', encoding='utf-8') as f_out:
        tweets = iter(from_tweet_js_file('twitter-2021-02-23-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680/data/tweet.js'))

        json.dump(list(filter(is_zh_tweet, filter(tweets_date_interval, tweets))), f_out, indent=2,
                  ensure_ascii=False)
