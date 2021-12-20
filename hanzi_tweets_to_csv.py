import argparse
import csv
import pathlib
from hanzi_helpers import next_hanzi_tweet_summarized, HanziTweetSummary


def generate_hanzi_tweets_csv(tweets_js_path: str, csv_output_path: str):
    summary_tweets = [tweet.to_dict() for tweet in next_hanzi_tweet_summarized(tweets_js_path)]
    summary_tweets.sort(key=lambda tw: tw["Date"], reverse=True)

    with open(csv_output_path, "w", newline='', encoding='utf-8') as csv_out:
        csv_wrtr = csv.DictWriter(csv_out, fieldnames=HanziTweetSummary.field_names(), quoting=csv.QUOTE_ALL)
        csv_wrtr.writeheader()
        for tw in summary_tweets:
            csv_wrtr.writerow(tw)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate markdown files of Chinese=text tweets")
    parser.add_argument('-tweet-js-path', type=str, required=True, help='twitter\'s tweet.js filepath')
    parser.add_argument('-summary-csv-path', type=str, required=True, help='summary tweets output csv path')
    args = parser.parse_args()
    generate_hanzi_tweets_csv(args.tweet_js_path, args.summary_csv_path)
