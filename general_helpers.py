from collections import Counter
from collections.abc import Sequence
from typing import Dict, Generator, List, Optional
from zoneinfo import ZoneInfo
import datetime
import json
import string


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
