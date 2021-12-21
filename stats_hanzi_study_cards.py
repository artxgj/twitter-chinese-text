import argparse
import pathlib
from hanzi_helpers import next_vocab_tweets_index
from simple_markdown import h1, table_row, table_header, link, MdCellAlign


def generate_vocab_tweets_stats(*, vocab_tweets_index_path: str,
                                cards_study_folder: str):
    vocab_tweets = [(row['Word'], len(row['Tweet_Ids'].split(',')))
                    for row in next_vocab_tweets_index(vocab_tweets_index_path)]
    vocab_tweets.sort(key=lambda data: data[1], reverse=True)
    fields = ['Rank', 'Word/Name', 'Number of Tweets']
    fields_align = [MdCellAlign.left, MdCellAlign.center, MdCellAlign.center]
    with open(f"{cards_study_folder}/words_tweets_stats.md", "w", encoding='utf-8') as f_out:
        md_static_part = f"""{h1('Study Words/Names Statistics')}
        
{table_header(fields, fields_align)}
"""
        f_out.writelines(md_static_part)
        rank = 1
        for word, num_tweets in vocab_tweets:
            row = [str(rank), link(word, f"{word}.md"), str(num_tweets)]
            f_out.writelines(f"{table_row(row)}\n")
            rank += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="generate vocabulary study cards")
    parser.add_argument('-vocab-tweets-index-path', type=str, required=True, help='words path file')
    parser.add_argument('-cards-study-path', type=str, required=True, help='cards folder')

    args = parser.parse_args()
    generate_vocab_tweets_stats(vocab_tweets_index_path=args.vocab_tweets_index_path,
                                cards_study_folder=args.cards_study_path)
