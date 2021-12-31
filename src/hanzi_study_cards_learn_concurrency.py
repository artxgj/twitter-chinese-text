import argparse
import logging
import pathlib

from typing import List
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from hanzi_helpers import cache_tweetid_words_csv, cache_tweets_summary_csv, next_vocab_tweets_index
from general_helpers import mdbg_link, wiktionary_link, googtrans_link
from simple_markdown import h1, h3, h5, hr, link, blockquote

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

_TWEETS_PER_PAGE = 400


@dataclass
class WordAndTweets:
    word: str
    tweet_ids: List[str]


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
    pure function to return link
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


def new_write_word_card(summarized_tweets_words: Mapping[str, Mapping],
                        cards_study_folder: str, tweets_per_page: int,
                        word_tweets: WordAndTweets):
    tweet_data = [summarized_tweets_words[tweet_id] for tweet_id in word_tweets.tweet_ids]
    tweet_data.sort(key=lambda tw: tw['Date'], reverse=True)
    num_tweets = len(tweet_data)
    title = word_tweets.word
    pages = (num_tweets // tweets_per_page) + (1 if num_tweets % tweets_per_page > 0 else 0)
    logging.info(f"Generating {title}, number of tweets {len(tweet_data)}, pages = {pages}")
    tweets_title_heading = f"Tweets containing {title}"
    word_static_md_part = f"""{h1(title)}

Search {link('mdbg', mdbg_link(title=title))} for definition

Search {link('wiktionary', wiktionary_link(title=title))} for definition

{h3(tweets_title_heading)}

"""
    for page in range(pages):
        word_md_filepath = f"{cards_study_folder}/{word_md_filename(title=title, page=page)}"
        logging.info(f"page {page}, pages {pages}, {word_md_filepath}")
        with open(word_md_filepath, "w", encoding='utf-8') as f_out:
            link_text = word_previous_next_links(title=title, page=page, pages=pages)

            md_page_buffer = [f"{link_text}\n{word_static_md_part}" if link_text else word_static_md_part]
            low = page * tweets_per_page
            last = low + tweets_per_page
            high = num_tweets if last > num_tweets else last

            for i in range(low, high):
                tweet = tweet_data[i]
                date_source = f"{tweet['Date']} ~ {tweet['Source']}"
                tweet_text = tweet['Tweet']
                md_tweet_body = f"""{hr()}

{h5(date_source)}

{blockquote(tweet['Tweet'])}

{link('Google Translation', googtrans_link(source_text=tweet_text))}

"""
                md_page_buffer.append(md_tweet_body)

                if len(tweet['Words']) > 1:
                    buffer = []
                    other_words = sorted(tweet['Words'].difference({title}))

                    for other_word in other_words:
                        buffer.append(link(other_word, f"{other_word}.md"))

                    md_other_words = f"""{h5('Other Words/Names of Interest in the Above Tweet')}

{', '.join(buffer)}

"""
                    md_page_buffer.append(md_other_words)

            if link_text:
                md_bottom_link = f"""____

{link_text}

"""
                md_page_buffer.append(md_bottom_link)

            f_out.writelines(md_page_buffer)


def single_threaded(summarized_tweets_words: Mapping[str, Mapping],
                    cards_study_folder: str,
                    tweets_per_page: int,
                    word_and_tweets_seq: Sequence[WordAndTweets]):
    for wt in word_and_tweets_seq:
        new_write_word_card(summarized_tweets_words,
                        cards_study_folder,
                        tweets_per_page, wt)


def multithr_poolexec(summarized_tweets_words: Mapping[str, Mapping],
                       cards_study_folder: str,
                       tweets_per_page: int,
                       word_and_tweets_seq: Sequence[WordAndTweets]):
    """
    no perf gain over single_threaded version, seems a tad slower too.

    :param summarized_tweets_words:
    :param cards_study_folder:
    :param tweets_per_page:
    :param word_and_tweets_seq:
    :return:
    """
    with ThreadPoolExecutor() as executor:
        fn = partial(new_write_word_card, summarized_tweets_words,
                     cards_study_folder, tweets_per_page)

        # Executes fn concurrently using threads on the links iterable. The
        # timeout is for the entire process, not a single call, so downloading
        # all images must complete within 30 seconds.
        executor.map(fn, word_and_tweets_seq, timeout=30)


def multiproc_poolexec(summarized_tweets_words: Mapping[str, Mapping],
                       cards_study_folder: str,
                       tweets_per_page: int,
                       word_and_tweets_seq: Sequence[WordAndTweets]):
    """
    slowest version
    :param summarized_tweets_words:
    :param cards_study_folder:
    :param tweets_per_page:
    :param word_and_tweets_seq:
    :return:
    """
    with ProcessPoolExecutor() as executor:
        fn = partial(new_write_word_card, summarized_tweets_words,
                     cards_study_folder, tweets_per_page)

        # Executes fn concurrently using threads on the links iterable. The
        # timeout is for the entire process, not a single call, so downloading
        # all images must complete within 30 seconds.
        executor.map(fn, word_and_tweets_seq, timeout=30)


if __name__ == '__main__':
    """
    This program is for learning the basics of Python concurrency models and to understand when 
    to use them.
    """

    import time
    ts = time.time()

    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="generate vocabulary study cards")
    parser.add_argument('-summary-csv-path', type=str, required=True, help='summary tweets csv path')
    parser.add_argument('-tweets-vocab-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-vocab-tweets-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-cards-study-path', type=str, required=True, help='cards folder')

    args = parser.parse_args()
    tweets_summary = cache_tweets_summary_csv(filepath=args.summary_csv_path)
    tweetid_words = cache_tweetid_words_csv(filepath=args.tweets_vocab_index_path)

    for tweet_id, words in tweetid_words.items():
        tweets_summary[tweet_id]['Words'] = words

    word_tweetids_list = [WordAndTweets(row['Word'], row['Tweet_Ids'].split(','))
                          for row in next_vocab_tweets_index(args.vocab_tweets_index_path)]

    #cardfn_ver = single_threaded
    cardfn_ver = multithr_poolexec
    #cardfn_ver = multiproc_poolexec

    cardfn_ver(summarized_tweets_words=tweets_summary,
               cards_study_folder=args.cards_study_path,
               tweets_per_page=_TWEETS_PER_PAGE,
               word_and_tweets_seq=word_tweetids_list)

    logging.info(f'Total time of make_cards: {time.time() - ts} seconds.')
