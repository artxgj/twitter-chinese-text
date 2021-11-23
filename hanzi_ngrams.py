import argparse
import csv
import pathlib
from general_helpers import NGramsCounter
from hanzi_helpers import HZTweetNgram, next_hanzi_tweet


def generate_ngram_csv(tweet_js_path: str, csv_prefix_path, ngram: int):
    ngrams_freq = NGramsCounter()
    tweet_ngrams = HZTweetNgram(ngram)

    for tweet in next_hanzi_tweet(tweet_js_path):
        ngrams_freq.add_ngrams(tweet_ngrams.extract(tweet))

    with open(f"{csv_prefix_path}/chinese-tweets-raw-{ngram}gram.csv", 'w') as outf:
        col1 = f"{ngram}gram"
        wrtr = csv.DictWriter(outf, fieldnames=(col1, "count"))
        wrtr.writeheader()
        for ngram, count in ngrams_freq.ngrams_counter.most_common():
            wrtr.writerow({col1: ngram, "count": count})


if __name__ == '__main__':
    tweet_js_filepath = f"./twitter-2021-10-21-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680/data/tweet.js"
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate csv file of 'raw' ngrams from tweets")

    parser.add_argument('-tweet-js-path', type=str, required=True, help='twitter\'s tweet.js filepath')
    parser.add_argument('-csv-prefix-path', type=str, required=True, help='csv output file path')
    parser.add_argument('-ngram', type=int, required=True, help='[n]gram')
    args = parser.parse_args()
    generate_ngram_csv(args.tweet_js_path, args.csv_prefix_path, args.ngram)

