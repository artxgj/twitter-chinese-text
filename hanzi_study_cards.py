import argparse
import pathlib
from general_helpers import dictlines_from_csv, googtrans_link
from generate_hanzi_tweets_indexes import FIELDNAMES_VOCAB_TWEETS_INDEX, FIELDNAMES_TWEETS_VOCAB_INDEX
from collections.abc import Sequence
from collections import namedtuple
from pprint import pprint


SummaryTweetAttrs = namedtuple('SummaryTweetAttrs', ('date', 'source', 'text'))


def get_vocab_tweets_index(*, csv_filepath: str, sort=True) -> Sequence:
    index = []
    for row in dictlines_from_csv(csv_filepath, None):
        index.append((row[FIELDNAMES_VOCAB_TWEETS_INDEX[0]], row[FIELDNAMES_VOCAB_TWEETS_INDEX[1]].split(',')))

    if sort:
        index.sort(key=lambda x: x[0])

    return index


def get_summary_tweets(*, csv_filepath):
    summary_tweets = {row['Id']: SummaryTweetAttrs(row['Date'], row['Source'], row['Tweet'])
                      for row in dictlines_from_csv(csv_filepath, None)}
    return summary_tweets


def get_tweets_vocab_index(*, csv_filepath):
    return {row['Tweet_Id']: set(row['Words'].split(',')) for row in dictlines_from_csv(csv_filepath, None)}


def make_cards(*, tweets_summary_csv_path: str,
               tweets_vocab_index_path: str,
               vocab_tweets_index_path: str,
               cards_study_folder: str):

    vocab_tweets_index = get_vocab_tweets_index(csv_filepath=vocab_tweets_index_path)
    pprint(vocab_tweets_index)
    summary_tweets = get_summary_tweets(csv_filepath=tweets_summary_csv_path)
    pprint(summary_tweets)
    tweets_vocab_index = get_tweets_vocab_index(csv_filepath=tweets_vocab_index_path)
    pprint(tweets_vocab_index)
    print("...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="generate vocabulary study cards")
    parser.add_argument('-summary-csv-path', type=str, required=True, help='summary tweets csv path')
    parser.add_argument('-tweets-vocab-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-vocab-tweets-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-cards-study-path', type=str, required=True, help='cards folder')

    args = parser.parse_args()
    make_cards(tweets_summary_csv_path=args.summary_csv_path,
               tweets_vocab_index_path=args.tweets_vocab_index_path,
               vocab_tweets_index_path=args.vocab_tweets_index_path,
               cards_study_folder=args.cards_study_path)
