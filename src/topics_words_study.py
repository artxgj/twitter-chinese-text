import argparse
import pathlib
from src.hanzi_helpers import next_vocab_tweets_index, dictlines_from_csv
from simple_markdown import h1, table_row, table_header, link, MdCellAlign


def generate_companies_tweets_stats(*, vocab_tweets_index_path: str,
                                    topics_words_csv_path: str,
                                    topics_words_md_path: str):
    topics_words = []
    topics_words_index = {}

    for i, r in enumerate(dictlines_from_csv(topics_words_csv_path)):
        topics_words.append(r)
        topics_words_index[r['Word']] = i

    for row in next_vocab_tweets_index(vocab_tweets_index_path):
        if row['Word'] in topics_words_index:
            i = topics_words_index[row['Word']]
            topics_words[i]['tweets'] = len(row['Tweet_Ids'].split(','))

    fields = ['Word/Name', 'Number of Tweets', 'Meaning']
    fields_align = [MdCellAlign.left, MdCellAlign.left, MdCellAlign.center]
    with open(topics_words_md_path, "w", encoding='utf-8') as f_out:
        md_static_part = f"""{h1('Study Tweets Containing Topics/Words')}
        
{table_header(fields, fields_align)}
"""
        f_out.writelines(md_static_part)
        rank = 1
        for word in topics_words:
            hanzi = word['Word']
            row = [link(hanzi, f"{hanzi}.md"), str(word['tweets']), word['meaning']]
            f_out.writelines(f"{table_row(row)}\n")
            rank += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="generate topics/words study list.")
    parser.add_argument('-vocab-tweets-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-topics-words-csv-path', type=str, required=True, help='topics/words csv path')
    parser.add_argument('-topics-words-md-path', type=str, required=True, help='topics/words markdown path')

    args = parser.parse_args()
    generate_companies_tweets_stats(vocab_tweets_index_path=args.vocab_tweets_index_path,
                                    topics_words_csv_path=args.topics_words_csv_path,
                                    topics_words_md_path=args.topics_words_md_path)
