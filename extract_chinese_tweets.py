import json
from typing import Iterator, Generator
from tweetybird import TweetDict, from_tweet_js_file, TweetsDateInterval, Mentions, is_zh_tweet

Zh_Tweets_Sources = {
    'ChineseWSJ',
    'ChosunChinese',
    'FTChinese',
    'KBSChinese',
    'asahi_shinsen',
    'bbcchinese',
    'dw_chinese',
    'nanyangpres',
    'rijingzhongwen',
    'zaobaosg'
}


def extract_tweets(tweets: Iterator, retweet_origins: Mentions,
                   tweets_date_range: TweetsDateInterval) -> Generator:
    return (tweet for tweet in tweets if tweets_date_range(tweet) and retweet_origins(tweet))


def simplified_zh_tweet_source(tweet_dict: TweetDict) -> bool:
    tweet = tweet_dict['tweet']
    return True if 'entities' in tweet and \
                   'user_mentions' in tweet['entities'] and \
                   len(tweet['entities']['user_mentions']) > 0 and \
                   tweet['entities']['user_mentions'][0]['screen_name'] in Zh_Tweets_Sources \
        else False


if __name__ == '__main__':
    tweet_js_filepath = f"./twitter-2021-07-14-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680/data/tweet.js"
    tweets_date_interval = TweetsDateInterval("2020-05-01")
    with open('chinese_text_tweet.json', 'w', encoding='utf-8') as f_out:
        tweets = from_tweet_js_file(tweet_js_filepath)
        dtweets = filter(tweets_date_interval, tweets)
        zhtweets = filter(is_zh_tweet, dtweets)
        simplified_zhtweets = filter(simplified_zh_tweet_source, zhtweets)
        json.dump(
            list(simplified_zhtweets),
            f_out,
            indent=2,
            ensure_ascii=False)

