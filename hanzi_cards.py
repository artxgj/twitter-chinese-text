import argparse
import pathlib
from general_helpers import lines_from_textfile, dictlines_from_csv
from hanzi_helpers import HanziTweetSummary
from hanzi_tweets_to_md import HanziSummaryMdReport, HanziSummaryMdFields


def make_cards(*, tweets_summary_csv_path: str, words_path: str, cards_folder: str):
    for word in lines_from_textfile(filepath=words_path):
        report_data = []
        print(f"Generating card for {word}")
        for tweet_summary in dictlines_from_csv(csv_path=tweets_summary_csv_path,
                                                fieldnames=HanziTweetSummary.field_names()):

            if word in tweet_summary['Tweet']:
                report_data.append(HanziSummaryMdFields(tweet_date=tweet_summary['Date'],
                                                        tweet_source=tweet_summary['Source'],
                                                        tweet_text=tweet_summary['Tweet']))

        word_tweets_md = HanziSummaryMdReport(report_data=report_data)
        word_tweets_md.write(f"{cards_folder}/{word}.md", title=f"{word}")
        print(f"{word} card generated.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="generate markdown-formatted word-tweets")
    parser.add_argument('-summary-csv-path', type=str, required=True, help='summary tweets csv path')
    parser.add_argument('-words-path', type=str, required=True, help='words path file')
    parser.add_argument('-cards-folder', type=str, required=True, help='cards folder')

    args = parser.parse_args()
    make_cards(tweets_summary_csv_path=args.summary_csv_path,
               words_path=args.words_path,
               cards_folder=args.cards_folder)
