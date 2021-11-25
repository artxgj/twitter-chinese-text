import argparse
import pathlib
from hanzi_tweets_to_md import HanziSummaryMdReport


def make_cards(*, csvs_folder: str, cards_folder: str):
    csv_files = sorted([p.name for p in pathlib.Path(csvs_folder).glob('*.csv')], key=lambda csv_name: csv_name[:-4])

    for csv_file in csv_files:
        word_tweets_md = HanziSummaryMdReport.from_summary_csv(f"{csvs_folder}/{csv_file}")
        word = csv_file[:-4]  # ignore .csv suffix
        word_tweets_md.write(f"{cards_folder}/{word}.md", title=f"{word}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="generate markdown-formatted word-tweets")
    parser.add_argument('-csvfiles-folder', type=str, required=True, help='csv')
    parser.add_argument('-cards-folder', type=str, required=True, help='summary tweets output csv path')
    args = parser.parse_args()
    make_cards(csvs_folder=args.csvfiles_folder, cards_folder=args.cards_folder)
