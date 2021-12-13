import argparse
import pathlib
from hanzi_helpers import HanziTweetSummary
from general_helpers import lines_from_textfile, dictlines_from_csv, dictlines_to_csv
from collections import defaultdict, namedtuple
from pprint import pprint


def build_indexes(*, tweets_summary_csv_path: str, vocab_list_path: str, index_folder: str):
    """
    build indexes in memory (tweets data are small enough to fit in memory) and
    then write to files
    :param tweets_summary_csv_path:
    :param vocab_list_path:
    :param index_folder:
    :return:
    """
    vocab_list = [line for line in lines_from_textfile(vocab_list_path)]
    tweets_with_vocab = defaultdict(list)
    vocab_tweets_index = defaultdict(set)

    for tweet in dictlines_from_csv(tweets_summary_csv_path, HanziTweetSummary.field_names()):
        for word in vocab_list:
            if word in tweet['Tweet']:
                tweets_with_vocab[tweet['Id']].append(word)
                vocab_tweets_index[word].add(tweet['Id'])

    tw_words_iter = iter({"Tweet_Id": k, "Words": ','.join(v)} for k, v in tweets_with_vocab.items())
    dictlines_to_csv(f"{index_folder}/tweets_vocab_index.dat",
                     ("Tweet_Id", "Words"),
                     tw_words_iter)

    words_tweets_iter = iter({"Word": k, "Tweet_Ids": ','.join(v)} for k, v in vocab_tweets_index.items())
    dictlines_to_csv(f"{index_folder}/vocab_tweets_index.dat",
                     ("Word", "Tweet_Ids"),
                     words_tweets_iter)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="generate vocab and tweets indices (or tables)")
    parser.add_argument('-summary-csv-path', type=str, required=True, help='summary tweets csv path')
    parser.add_argument('-vocab-list-path', type=str, required=True, help='words path file')
    parser.add_argument('-index-path', type=str, required=True)
    args = parser.parse_args()
    build_indexes(tweets_summary_csv_path=args.summary_csv_path,
                  vocab_list_path=args.vocab_list_path,
                  index_folder=args.index_path)
