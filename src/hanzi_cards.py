import argparse
import logging
import pathlib
from general_helpers import lines_from_textfile, dictlines_from_csv
from hanzi_tweets_to_md import HanziSummaryMdReport, HanziSummaryMdFields

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def make_cards(*, tweets_summary_csv_path: str, words_path: str, cards_folder: str):
    for word in lines_from_textfile(filepath=words_path):
        print(f"Generating card for {word}")
        word_tweets_md = HanziSummaryMdReport.make_word_based_tweets(word, tweets_summary_csv_path)
        word_tweets_md.write(f"{cards_folder}/{word}.md", title=f"{word}")
        print(f"{word} card generated.")


if __name__ == '__main__':
    import time
    ts = time.time()

    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="generate markdown-formatted word-tweets")
    parser.add_argument('-summary-csv-path', type=str, required=True, help='summary tweets csv path')
    parser.add_argument('-words-path', type=str, required=True, help='words path file')
    parser.add_argument('-cards-folder', type=str, required=True, help='cards folder')

    args = parser.parse_args()

    make_cards(tweets_summary_csv_path=args.summary_csv_path,
               words_path=args.words_path,
               cards_folder=args.cards_folder)

    logging.info(f'Total time of make_cards: {time.time() - ts} seconds.')
