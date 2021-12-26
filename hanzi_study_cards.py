import argparse
import pathlib
from hanzi_helpers import next_tweets_vocab_index, next_vocab_tweets_index, next_HanziTweetSummary
from general_helpers import mdbg_link, wiktionary_link, googtrans_link
from simple_markdown import h1, h3, h5, hr, link, blockquote
from typing import List
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass
class WordAndTweets:
    word: str
    tweet_ids: List[str]


_TWEETS_PER_PAGE = 400


def cache_tweetsummary_words(*, tweet_summary_csv_filepath: str,
                             tweets_vocab_csv_filepath: str):
    cache = dict()
    for row in next_HanziTweetSummary(tweet_summary_csv_filepath):
        cache[row['Id']] = {
            'Date': row['Date'],
            'Source': row['Source'],
            'Tweet': row['Tweet']
        }

    for row in next_tweets_vocab_index(tweets_vocab_csv_filepath):
        cache[row['Tweet_Id']]['Words'] = set(row['Words'].split(','))

    return cache


def cache_vocab_tweets_index(*, vocab_tweets_index_path: str):
    return [WordAndTweets(row['Word'], row['Tweet_Ids'].split(','))
            for row in next_vocab_tweets_index(vocab_tweets_index_path)]


def word_md_filename(*, title: str, page: int) -> str:
    """

    :param title: word
    :param page: zero-based
    :param pages: total number of pages for title
    :return:
    """
    return f"{title}-{page:02}.md" if page > 0 else f"{title}.md"


def word_previous_next_links(*, title: str, page: int, pages: int) -> str:
    """

    :param title:
    :param page: zero-based
    :param pages: total number of pages
    :return:
    """
    if pages == 1:
        return ''

    next_page = link("Next Page", f"{title}-{page+1:02}.md")
    prev_page = link("Previous Page", word_md_filename(title=title, page=page-1))

    if page == 0:
        return next_page
    elif page == pages - 1:
        return prev_page
    else:
        return f"{prev_page} | {next_page}"


def write_word_card(*, title: str, tweet_data: List[Mapping[str, Mapping]], cards_study_folder: str,
                    tweets_per_page: int):
    num_tweets = len(tweet_data)
    pages = (num_tweets // tweets_per_page) + (1 if num_tweets % tweets_per_page > 0 else 0)
    print(f"Generating {title}, number of tweets {len(tweet_data)}, pages = {pages}")
    tweets_title_heading = f"Tweets containing {title}"
    word_static_md_part = f"""{h1(title)}

Search {link('mdbg', mdbg_link(title=title))} for definition

Search {link('wiktionary', wiktionary_link(title=title))} for definition

{h3(tweets_title_heading)}

"""
    for page in range(pages):
        word_md_filepath = f"{cards_study_folder}/{word_md_filename(title=title, page=page)}"
        print(f"page {page}, pages {pages}, {word_md_filepath}")
        with open(word_md_filepath, "w", encoding='utf-8') as f_out:
            link_text = word_previous_next_links(title=title, page=page, pages=pages)

            if link_text:
                f_out.write(f"{link_text}\n")

            f_out.writelines(word_static_md_part)
            low = page * tweets_per_page
            last = low + tweets_per_page
            high = num_tweets if last > num_tweets else last

            for i in range(low, high):
                tweet = tweet_data[i]
                f_out.write(f"{hr()}\n")
                date_source = f"{tweet['Date']} ~ {tweet['Source']}"
                f_out.write(f"{h5(date_source)}\n")
                tweet_text = tweet['Tweet']
                f_out.write(f"{blockquote(tweet_text)}\n")
                f_out.write(f"\n{link('Google Translation', googtrans_link(source_text=tweet_text))}\n")

                if len(tweet['Words']) > 1:
                    f_out.write(f"{h5('Other Words/Names of Interest in the Above Tweet')}\n")
                    buffer = []
                    other_words = sorted(tweet['Words'].difference({title}))

                    for other_word in other_words:
                        buffer.append(link(other_word, f"{other_word}.md"))

                    f_out.write(f"{', '.join(buffer)}\n")

            if link_text:
                f_out.write(f"____\n\n{link_text}\n")


def write_cards(*, word_and_tweets: List[WordAndTweets],
                summarized_tweets_words: Mapping[str, Mapping],
                cards_study_folder: str,
                tweets_per_page: int):

    for word_tweets in word_and_tweets:
        tweet_data = [summarized_tweets_words[tweet_id] for tweet_id in word_tweets.tweet_ids]
        tweet_data.sort(key=lambda tw: tw['Date'], reverse=True)
        write_word_card(title=word_tweets.word, tweet_data=tweet_data,
                        cards_study_folder=cards_study_folder,
                        tweets_per_page=tweets_per_page)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="generate vocabulary study cards")
    parser.add_argument('-summary-csv-path', type=str, required=True, help='summary tweets csv path')
    parser.add_argument('-tweets-vocab-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-vocab-tweets-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-cards-study-path', type=str, required=True, help='cards folder')

    args = parser.parse_args()
    summarized_tweets_study_words = cache_tweetsummary_words(tweet_summary_csv_filepath=args.summary_csv_path,
                                                             tweets_vocab_csv_filepath=args.tweets_vocab_index_path)
    word_and_tweets = cache_vocab_tweets_index(vocab_tweets_index_path=args.vocab_tweets_index_path)

    print("===========")

    write_cards(word_and_tweets=word_and_tweets,
                summarized_tweets_words=summarized_tweets_study_words,
                cards_study_folder=args.cards_study_path,
                tweets_per_page=_TWEETS_PER_PAGE)
