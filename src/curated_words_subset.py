import pytomlpp as toml
import argparse
import pathlib
from simple_markdown import h1, h2, table_row, table_header, link, MdCellAlign
from pprint import pprint
from general_helpers import JIANTI_FANTI_DELIM


def generate_curated_words_study(*, words_toml_path: str,
                                 curated_words_study_path: str):
    _md_template = [f"""{h1(f"A Subset of Curated Words Extracted From Tweets")}

To learn how the words are used in context, read the tweets by clicking or tapping on the Chinese words. For a complete 
list of the curated words, check it out {link('here', 'words_tweets_stats.md')}.
"""]

    toml_words = toml.load(words_toml_path)
    fields_align = [MdCellAlign.left, MdCellAlign.center]
    pprint(toml_words)
    for name, heading in toml_words['category-names'].items():
        _md_template.append(h2(heading))
        _md_template.append(table_header(['', ''], fields_align))
        for word in toml_words[name]:
            hz_words = word['hz'].split(JIANTI_FANTI_DELIM)
            hz_heading = JIANTI_FANTI_DELIM.join([link(hz_word, f"{hz_word}.md") for hz_word in hz_words])
            _md_template.append(table_row([hz_heading, word['en']]))

    with open(curated_words_study_path, "w") as fh:
        fh.writelines('\n'.join(_md_template))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="generate vocabulary study cards")
    parser.add_argument('-words-toml-path', type=str, required=True, help='curated words toml file')
    parser.add_argument('-curated-words-study-path', type=str, required=True, help='curated words study filepath')
    args = parser.parse_args()
    generate_curated_words_study(words_toml_path=args.words_toml_path,
                                 curated_words_study_path=args.curated_words_study_path)

