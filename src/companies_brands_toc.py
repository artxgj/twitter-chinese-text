import argparse
import pathlib

from simple_markdown import h1, table_row, table_header, link, MdCellAlign
from src.hanzi_helpers import next_vocab_tweets_index, dictlines_from_csv
from src.general_helpers import JIANTI_FANTI_DELIM

def generate_companies_tweets_stats(*, vocab_tweets_index_path: str,
                                    cards_study_folder: str,
                                    companies_csv_path: str):
    companies_tickers = []
    companies_index = {}

    for i, r in enumerate(dictlines_from_csv(companies_csv_path)):
        r['tweets'] = 0
        companies_tickers.append(r)
        for hz_name in r['Chinese Name'].split(JIANTI_FANTI_DELIM):
            companies_index[hz_name] = i

    for row in next_vocab_tweets_index(vocab_tweets_index_path):
        if row['Word'] in companies_index:
            i = companies_index[row['Word']]
            companies_tickers[i]['tweets'] += len(row['Tweet_Ids'].split(','))

    fields = ['Chinese Name', 'English Name', 'U.S. Ticker', 'Number of Tweets']
    fields_align = [MdCellAlign.left, MdCellAlign.left, MdCellAlign.center, MdCellAlign.center]
    with open(f"{cards_study_folder}/companies_tweets_stats.md", "w", encoding='utf-8') as f_out:
        md_static_part = f"""{h1('Companies/Brands')}

{table_header(fields, fields_align)}
"""
        f_out.writelines(md_static_part)
        rank = 1
        for company in companies_tickers:
            hz_names = company['Chinese Name'].split(JIANTI_FANTI_DELIM)
            print(company)
            try:
                company_links = JIANTI_FANTI_DELIM.join([link(hanzi, f"{hanzi}.md") for hanzi in hz_names])
                row = [company_links, company['English Name'], company['Ticker'], str(company['tweets'])]
                f_out.writelines(f"{table_row(row)}\n")
                rank += 1
            except KeyError as err:
                print(f"KeyError: {err}")


if __name__=='__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
        description="generate vocabulary study cards")
    parser.add_argument('-vocab-tweets-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-companies-csv-path', type=str, required=True, help='words path file')
    parser.add_argument('-cards-study-path', type=str, required=True, help='cards folder')

    args = parser.parse_args()
    generate_companies_tweets_stats(vocab_tweets_index_path=args.vocab_tweets_index_path,
                                    cards_study_folder=args.cards_study_path,
                                    companies_csv_path=args.companies_csv_path)
