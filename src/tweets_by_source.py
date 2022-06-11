from twitter_objects import from_tweet_js_file, next_tweet


def tweets_by_source(tweet_js_path, source):
    for tweet in next_tweet(from_tweet_js_file(tweet_js_path)):
        if len(tweet.user_mentions) > 0 and tweet.user_mentions[0].name == source:
            print(tweet.full_text)
            print()


if __name__ == '__main__':
    tweet_js_path = '../twitter-2022-06-11-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680/data/tweet.js'
    tweets_by_source(tweet_js_path, 'FabulousAniyyah')

