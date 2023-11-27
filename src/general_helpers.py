import csv
import datetime
import json
import string
import urllib.parse
from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Dict, Generator, Iterator, List, Optional
from zoneinfo import ZoneInfo


JIANTI_FANTI_DELIM = '/'


def from_file_collection_json(filepath: str) -> Generator[Dict, None, None]:
    """
    collection refers to an array of json objects
    """
    with open(filepath, "r") as f_in:
        collection = json.load(f_in)
        for json_dict in collection:
            yield json_dict


def from_collection_json(json_seq: Sequence) -> Generator[Dict, None, None]:
    for elem in json_seq:
        yield elem


def dictlines_from_csv(csv_path: str,
                       fieldnames: Optional[Sequence[str]] = None,
                       encoding: str = 'utf-8') -> Generator[Mapping, None, None]:
    with open(csv_path, 'r', encoding=encoding) as csv_stream:
        rdr = csv.DictReader(csv_stream, fieldnames)
        for row in rdr:
            yield row


def dictlines_to_csv(csv_path: str, fieldnames, dictlines: Iterator[dict], encoding: str = 'utf-8'):
    with open(csv_path, 'w', encoding=encoding) as ostream:
        wrtr = csv.DictWriter(ostream, fieldnames=fieldnames)
        wrtr.writeheader()

        for row in dictlines:
            wrtr.writerow(row)


def lines_from_textfile(filepath: str, encoding: str = 'utf-8') -> str:
    with open(filepath, 'r', encoding=encoding) as istream:
        for line in istream:
            yield line.strip()


class DateInterval:
    def __init__(self, start_date: str, end_date: Optional[str] = None, timezone=ZoneInfo("UTC")):
        self._start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").astimezone(timezone)

        if end_date is None:
            self._end_date = datetime.datetime.today().astimezone(timezone)
        else:
            self._end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").astimezone(timezone)

        assert self._start_date < self._end_date

    def __contains__(self, item: datetime.datetime):
        return self._start_date <= item <= self._end_date

    def __repr__(self):
        return f"date range: [{self._start_date}, {self._end_date}]"


_LETTER_DIGITS = set(string.digits + string.ascii_letters)


def is_letter_digit(c: str) -> bool:
    return c in _LETTER_DIGITS


class NGramsCounter:
    def __init__(self):
        self._counter = Counter()

    def add_ngrams(self, ngrams: List[str]):
        for ngram in ngrams:
            self.add_ngram(ngram)

    def add_ngram(self, ngram: str):
        self._counter[ngram] += 1

    @property
    def ngrams_counter(self):
        return self._counter


def googtrans_link(*, source_text: str, sl='zh-CN', tl='en') -> str:
    gt_params = {
        'hi': 'en',
        'tab': 'TT',
        'sl': sl,
        'tl': tl,
        'op': 'translate',
        'text': source_text.replace('\n', '')
    }

    return f"https://translate.google.com/?{urllib.parse.urlencode(gt_params)}"


def wiktionary_link(*, title: str) -> str:
    return f"https://en.wiktionary.org/wiki/{title}"


def pleco_link(*, title: str, return_app: str, return_url: str) -> str:
    return f"plecoapi://x-callback-url/df?hw=({title})&py=pinyin&sec=dict&x-source={return_app}" \
           f"&x-success=({return_url})"


def mdbg_link(*, title):
    return f"https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb={title}"
