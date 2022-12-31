import argparse
import csv
import datetime
import pathlib
from collections import defaultdict
from general_helpers import NGramsCounter
from hanzi_helpers import HZTweetNgram, next_hanzi_tweet, valid_tweet_input_date


def generate_ngram_csv(tweet_js_path: str, csv_prefix_path, ngram: int,
                       start_date: datetime.datetime, end_date: datetime.datetime,
                       ignore_ids: set = None):
    ngrams_freq = NGramsCounter()
    tweet_ngrams = HZTweetNgram(ngram)
    ngram_tweets_count = defaultdict(int)

    if ignore_ids is None:
        ignore_ids = set()

    for tweet in next_hanzi_tweet(tweet_js_path):
        if tweet.id_int in ignore_ids:
            continue

        if isinstance(start_date, datetime.datetime) and isinstance(end_date, datetime.datetime) and \
                (tweet.created_at < start_date or tweet.created_at > end_date):
            continue

        ngrams_of_tweet = tweet_ngrams.extract(tweet)
        unique_ngrams_of_tweet = set(ngrams_of_tweet)
        for 詞 in unique_ngrams_of_tweet:
            ngram_tweets_count[詞] += 1

        ngrams_freq.add_ngrams(ngrams_of_tweet)

    # quick and dirty change
    # create a list of 3-tuples representing (number of tweets, total number of occurrences, word)
    # then sort by descending

    ngrams_stats = [(ngram_tweets_count[zhgram], count, zhgram) for zhgram, count in
                    ngrams_freq.ngrams_counter.most_common()]

    ngrams_stats.sort(reverse=True)

    with open(f"{csv_prefix_path}/chinese-tweets-raw-{ngram}gram.csv", 'w') as outf:
        col1 = f"{ngram}gram"
        wrtr = csv.DictWriter(outf, fieldnames=(col1, "number of tweets", "count"), quoting=csv.QUOTE_ALL)
        wrtr.writeheader()
        for tweets, count, 詞 in ngrams_stats:
            wrtr.writerow({col1: 詞, "number of tweets": tweets, "count": count, })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate csv file of 'raw' ngrams from tweets")
    parser.add_argument('-tweet-js-path', type=str, required=True, help='twitter\'s tweet.js filepath')
    parser.add_argument('-csv-prefix-path', type=str, required=True, help='csv output file path')
    parser.add_argument('-ngram', type=int, required=True, help='[n]gram')
    parser.add_argument('-start-date',
                        type=valid_tweet_input_date,
                        default=None,
                        required=False,
                        help='start date in format "YYYY-MM-DD"')

    parser.add_argument('-end-date',
                        type=valid_tweet_input_date,
                        default=None,
                        required=False,
                        help='end date in format "YYYY-MM-DD')

    args = parser.parse_args()
    print(args)

    if args.start_date and args.end_date and args.end_date <= args.start_date:
        raise ValueError(f"end_date ({args.end_date}) must be > start_date ({args.start_date}).")

    generate_ngram_csv(tweet_js_path=args.tweet_js_path,
                       csv_prefix_path=args.csv_prefix_path,
                       ngram=args.ngram,
                       start_date=args.start_date,
                       end_date=args.end_date,
                       ignore_ids={1527428219283984385, 1381845750619852800,
                                   1373710194467762178})

