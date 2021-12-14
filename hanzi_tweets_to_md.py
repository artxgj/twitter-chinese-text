import argparse
import csv
import datetime
import pathlib

import simple_markdown as md
from dataclasses import dataclass
from typing import List
from general_helpers import dictlines_from_csv, googtrans_link
from hanzi_helpers import next_hanzi_summary_tweet, HanziTweetSummary


@dataclass
class HanziSummaryMdFields:
    tweet_date: str
    tweet_source: str
    tweet_text: str


class HanziSummaryMdReport:
    def __init__(self, report_data: List[HanziSummaryMdFields]):
        self._report_data = report_data

    def write(self, md_filepath: str, title: str, reverse_sort: bool = True):
        self._report_data.sort(key=lambda tw: tw.tweet_date, reverse=reverse_sort)
        mdtb_rows = []

        for attrs in self._report_data:
            link = googtrans_link(source_text=attrs.tweet_text)
            mdtb_rows.append(md.table_row([str(attrs.tweet_date), attrs.tweet_source, md.link(attrs.tweet_text, link)]))

        tbl = '\n'.join(mdtb_rows)
        report = f"""## {title} 

Tweets with [{title}](https://en.wiktionary.org/wiki/{title}). Tap or click to check if Wiktionary has an entry for it.

| UTC Date | Tweet Source | Tweet (click or tap to see Google Translation) |
|:-----------------|:-------------|:------------------|  
{tbl}
"""
        with open(md_filepath, "w") as f_out:
            f_out.writelines(report)

    @classmethod
    def _date_str(cls, date_obj: datetime.datetime):
        return date_obj.strftime("%Y-%m-%d %H:%M:%S %Z")

    @classmethod
    def from_tweet_js(cls, tweet_js_path: str):
        return cls([HanziSummaryMdFields(tweet_date=cls._date_str(tw.tweet_date),
                                         tweet_source=tw.tweet_source,
                                         tweet_text=tw.tweet_text)
                    for tw in next_hanzi_summary_tweet(tweet_js_path)])

    @classmethod
    def make_word_based_tweets(cls, word: str, summary_tweets_csv_path: str):
        report_data = []
        for tweet_summary in dictlines_from_csv(csv_path=summary_tweets_csv_path,
                                                fieldnames=HanziTweetSummary.field_names()):

            if word in tweet_summary['Tweet']:
                report_data.append(HanziSummaryMdFields(tweet_date=tweet_summary['Date'],
                                                        tweet_source=tweet_summary['Source'],
                                                        tweet_text=tweet_summary['Tweet']))

        return cls(report_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate markdown files of Chinese=text tweets")
    parser.add_argument('-tweet-js-path', type=str, required=True, help='twitter\'s tweet.js filepath')
    parser.add_argument('-md-report-path', type=str, required=True, help='markdown output report filepath')
    parser.add_argument('-title', type=str, required=True, help='title of report')
    args = parser.parse_args()

    md_report = HanziSummaryMdReport.from_tweet_js(args.tweet_js_path)
    md_report.write(args.md_report_path, args.title)
