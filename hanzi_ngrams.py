from hanzi_helpers import NGramsCounter, HZTweetNgram
from twitter_objects import from_tweet_js_file, next_tweet, is_tweet_in_sources
from pprint import pprint


if __name__ == '__main__':
    ngrams_freq = NGramsCounter()
    tweet_ngrams = HZTweetNgram(9)
    tweet_js_filepath = f"./twitter-2021-10-21-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680/data/tweet.js"

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

    for tweet in next_tweet(from_tweet_js_file(tweet_js_filepath)):
        if is_tweet_in_sources(tweet, Zh_Tweets_Sources):
            ngrams_freq.add_ngrams(tweet_ngrams.extract(tweet))

    pprint(ngrams_freq.ngrams_counter)
