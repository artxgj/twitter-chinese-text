import argparse
import csv
import pathlib

from hanzi_helpers import next_hanzi_tweet
from twitter_objects import AbbreviatedTweet
from typing import List


def generate_hanzi_tweets_csv(tweets_js_path: str, csv_output_path: str):
    summary_tweets = [ {"Date": tweet.created_at.strftime("%Y-%m-%d"),
                        "Id": tweet.id_int, "Source": tweet.user_mentions[0].name,
                        "Tweet": tweet.full_text.replace('\n', '')} for tweet in next_hanzi_tweet(tweets_js_path)]

    summary_tweets.sort(key=lambda tw: tw["Date"], reverse=True)

    with open(csv_output_path, "w") as csv_out:
        csv_wrtr = csv.DictWriter(csv_out, fieldnames=("Date", "Id", "Source", "Tweet"), quoting=csv.QUOTE_ALL)
        csv_wrtr.writeheader()
        for tw in summary_tweets:
            csv_wrtr.writerow(tw)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate markdown files of Chinese=text tweets")
    parser.add_argument('-tweet-js-path', type=str, required=True, help='twitter\'s tweet.js filepath')
    args = parser.parse_args()
    generate_hanzi_tweets_csv(args.tweet_js_path, "csv/summary_tweets_chinese_text.csv")
