import argparse
import csv
import json
import pathlib

from tweets_ngrams import HZTweetNgram, NGramsCounter


def generate_ngram_csv(json_path: str, csv_prefix_path, ngram: int):
    ngrams_freq = NGramsCounter()
    tweet_ngrams = HZTweetNgram(ngram)

    with open(json_path, 'r') as fp:
        tweets = json.load(fp)
        for tweet in tweets:
            ngrams_freq.add_ngrams(tweet_ngrams.extract(tweet))

    with open(f"{csv_prefix_path}-{ngram}gram.csv", 'w') as outf:
        col1 = f"{ngram}gram"
        wrtr = csv.DictWriter(outf, fieldnames=(col1, "count"))
        wrtr.writeheader()
        for ngram, count in ngrams_freq.ngrams_counter.most_common():
            wrtr.writerow({col1: ngram, "count": count})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate csv file of 'raw' ngrams from tweets")

    parser.add_argument('-json-path', type=str, required=True, help='chinese-text tweets json file')
    parser.add_argument('-csv-prefix-path', type=str, required=True, help='csv output file path')
    parser.add_argument('-ngram', type=int, required=True, help='[n]gram')
    args = parser.parse_args()
    generate_ngram_csv(args.json_path, args.csv_prefix_path, args.ngram)
