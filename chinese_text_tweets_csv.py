import json
import datetime
import csv
from typing import Generator, Tuple
from tweetybird import tweet_full_text, tweet_user_mentions, tweet_date, tweet_id, TWITTER_DATE_FORMAT


def from_twitter_json_file(filepath: str) -> Generator[Tuple[str, str, str], None, None]:
    with open(filepath, "r") as f_in:
        tweets = json.load(f_in)
        for tweet in tweets:
            dt_tweet = datetime.datetime.strptime(tweet_date(tweet), TWITTER_DATE_FORMAT).strftime("%Y-%m-%d")
            yield dt_tweet, tweet_id(tweet), tweet_user_mentions(tweet), tweet_full_text(tweet)


def tweets_simplified_csv(summary_tweets: Generator[Tuple[str, str, str], None, None], csv_filepath: str):
    sorted_tweets = sorted(summary_tweets, key=lambda twt: twt[0], reverse=True)
    with open(csv_filepath, "w") as f_out:
        csv_wrtr = csv.DictWriter(f_out, fieldnames=("Date", "Id", "Source", "Tweet"), quoting=csv.QUOTE_ALL)
        csv_wrtr.writeheader()

        for tw_date, tw_id, source, tweet_text in sorted_tweets:
            csv_wrtr.writerow({"Date": tw_date, "Id": tw_id, "Source": source, "Tweet": tweet_text })


if __name__ == '__main__':
    tweets_simplified_csv(from_twitter_json_file("chinese_text_tweet.json"), "study/summary_tweets_chinese_text.csv")
