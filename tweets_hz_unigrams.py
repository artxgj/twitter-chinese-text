import json
from tweetybird import tweet_text_minus_entities, tweet_hashtags_text
from cjk_latin_emoji import RE_SEPARATORS, is_cjk, is_letter_digit
from collections import Counter
from csv import DictWriter


def tweets_hz_unigrams(tweets_json_filepath: str) -> Counter[str, int]:
    code_points: Counter[str, int] = Counter()
    hashtags: Counter[str, int] = Counter()
    with open(tweets_json_filepath) as fp:
        tweets = json.load(fp)
        for tweet in tweets:
            core_tweet = tweet_text_minus_entities(tweet)
            for tokens in RE_SEPARATORS.split(core_tweet):
                for token in tokens:
                    if is_cjk(token):
                        code_points[token] += 1
            for hashtag in tweet_hashtags_text(tweet):
                hashtags[hashtag] += 1

    for ht in hashtags:
        for c in ht:
            if is_cjk(c):
                code_points[c] += 1

    return code_points


def write_unigrams_csv(unigrams: Counter[str, int], filepath: str):
    with open(filepath, "w") as fp:
        csv_wrtr = DictWriter(fp, fieldnames=['word', 'frequency'])
        csv_wrtr.writeheader()
        for word, count in unigrams.most_common():
            csv_wrtr.writerow({'word': word, 'frequency': count})


if __name__ == '__main__':
    unigrams = tweets_hz_unigrams("chinese_text_tweet.json")
    write_unigrams_csv(unigrams, "study/tweets_unigrams.csv")
