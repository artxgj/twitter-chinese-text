import argparse
import pathlib
from general_helpers import dictlines_from_csv, googtrans_link, mdbg_link, wiktionary_link
from simple_markdown import ul, blockquote, link, hr, h1, h3
from collections.abc import Sequence
from collections import namedtuple


SummaryTweetAttrs = namedtuple('SummaryTweetAttrs', ('date', 'id', 'source', 'text'))


def get_summary_tweets(*, csv_filepath):
    summary_tweets = {row['Id']: SummaryTweetAttrs(row['Date'], row['Id'], row['Source'], row['Tweet'])
                      for row in dictlines_from_csv(csv_filepath, None)}
    return summary_tweets


def get_tweets_vocab_index(*, csv_filepath):
    return {row['Tweet_Id']: row['Words'].split(',') for row in dictlines_from_csv(csv_filepath, None)}


def md_quizcard(sum_tweet: SummaryTweetAttrs, words: Sequence[str]):

    quiz_words = []

    for word in words:
        mdbg = link('mdbg', mdbg_link(title=word))
        wikt = link('wiktionary', wiktionary_link(title=word))
        quiz_words.append(ul(f"{word} {mdbg} {wikt}"))

    ul_words = '\n'.join(quiz_words)
    title = f"{h1('Words/Names Review')}"
    qz_card = f"""
{title}
{hr()}
{ul_words }
{h3('Tweet')}
{sum_tweet.source} {sum_tweet.date}
{blockquote(sum_tweet.text)}

{link('Google Translation', googtrans_link(source_text=sum_tweet.text))}
"""
    return qz_card


def write_quizcard(review_quiz_folder: str, sum_tweet: SummaryTweetAttrs,
                   words: Sequence[str]):
    quizcard = md_quizcard(sum_tweet=sum_tweet, words=words)
    with open(f"{review_quiz_folder}/{sum_tweet.date[:10]}-{sum_tweet.id}.md", "w") as f:
        f.writelines(quizcard)
    print(md_quizcard(sum_tweet, words))


def make_cards(*, tweets_summary_csv_path: str,
               tweets_vocab_index_path: str,
               review_quiz_folder: str):

    summary_tweets = get_summary_tweets(csv_filepath=tweets_summary_csv_path)

    tweets_vocab_index = get_tweets_vocab_index(csv_filepath=tweets_vocab_index_path)

    for tweet_id, words in tweets_vocab_index.items():
        write_quizcard(review_quiz_folder, summary_tweets[tweet_id], words)

    print(len(summary_tweets), len(tweets_vocab_index))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="generate vocabulary study cards")
    parser.add_argument('-summary-csv-path', type=str, required=True, help='summary tweets csv path')
    parser.add_argument('-tweets-vocab-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-vocab-tweets-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-review-quiz-path', type=str, required=True, help='cards folder')

    args = parser.parse_args()
    make_cards(tweets_summary_csv_path=args.summary_csv_path,
               tweets_vocab_index_path=args.tweets_vocab_index_path,
               review_quiz_folder=args.review_quiz_path)
