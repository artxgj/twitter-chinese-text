import argparse
import csv
import datetime
import pathlib
import urllib.parse
import simple_markdown as md
from collections.abc import Sequence
from dataclasses import dataclass
from hanzi_helpers import next_hanzi_summary_tweet


@dataclass
class HanziSummaryMdFields:
    tweet_date: str
    tweet_source: str
    tweet_text: str


class HanziSummaryMdReport:
    def __init__(self, report_data: Sequence[HanziSummaryMdFields]):
        self._report_data = report_data

    def write(self, md_filepath: str, title: str, reverse_sort: bool = True):
        self._report_data.sort(key=lambda tw: tw.tweet_date, reverse=reverse_sort)
        gt_params = dict(hi='en', tab='TT', sl='zh-CN', tl='en', op='translate')
        mdtb_rows = []

        for attrs in self._report_data:
            norm_text = attrs.tweet_text.replace('\n', '')
            gt_params['text'] = norm_text
            link = f"https://translate.google.com/?{urllib.parse.urlencode(gt_params)}"
            mdtb_rows.append(md.table_row([str(attrs.tweet_date), attrs.tweet_source, md.link(norm_text, link)]))

        tbl = '\n'.join(mdtb_rows)
        report = f"""## {title}    
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
    def from_summary_csv(cls, csv_input_path: str):
        with open(csv_input_path, "r",  newline='', encoding='utf-8') as f_in:
            rdr = csv.reader(f_in,  delimiter=',')
            return cls([HanziSummaryMdFields(tweet_date=row[0],
                                             tweet_source=row[2],
                                             tweet_text=row[3])
                        for row in rdr])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate markdown files of Chinese=text tweets")
    parser.add_argument('-tweet-js-path', type=str, required=True, help='twitter\'s tweet.js filepath')
    parser.add_argument('-md-report-path', type=str, required=True, help='markdown output report filepath')
    parser.add_argument('-title', type=str, required=True, help='title of report')
    args = parser.parse_args()

    md_report = HanziSummaryMdReport.from_tweet_js(args.tweet_js_path)
    md_report.write(args.md_report_path, args.title)
