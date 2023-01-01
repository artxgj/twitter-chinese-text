import argparse
import datetime
import pathlib

import simple_markdown as md
from dataclasses import dataclass
from typing import List
from general_helpers import dictlines_from_csv, googtrans_link
from hanzi_helpers import next_hanzi_tweet, HanziTweetSummary, next_hanzi_tweet_summarized, HanziTweetSummary, valid_tweet_input_date, tweet_in_date_range


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
        report = f"""## Tweets {title}

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
    def from_tweet_js(cls, tweet_js_path: str,
                      start_date: datetime.datetime = None,
                      end_date: datetime.datetime = None):

        summary_md_fields = []
        for tw in next_hanzi_tweet(tweet_js_path):
            if tweet_in_date_range(tweet=tw,
                                   start_date=start_date,
                                   end_date=end_date):
                tw_summary = HanziTweetSummary(tw)
                summary_md_fields.append(HanziSummaryMdFields(tweet_date=cls._date_str(tw_summary.tweet_date),
                                         tweet_source=tw_summary.tweet_source,
                                         tweet_text=tw_summary.tweet_text))
        return cls(summary_md_fields)

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
    parser.add_argument('-start-date',
                        type=valid_tweet_input_date,
                        default=None,
                        required=False,
                        help='start date in format "YYYY-MM-DD"')

    parser.add_argument('-end-date',
                        type=valid_tweet_input_date,
                        default=None,
                        required=False,
                        help='end date in format "YYYY-MM-DD')

    args = parser.parse_args()

    filename = ""
    if args.start_date and args.end_date and args.end_date <= args.start_date:
        raise ValueError(f"end_date ({args.end_date}) must be > start_date ({args.start_date}).")
    elif args.start_date is None or args.end_date is None:
        filename = "tweets.md"
    else:
        filename = f"tweets-{args.start_date.strftime('%Y%m%d')}T{args.end_date.strftime('%Y%m%d')}.md"

    md_report_path = f"{args.md_report_path}/{filename}"
    md_report = HanziSummaryMdReport.from_tweet_js(args.tweet_js_path,
                                                   start_date=args.start_date,
                                                   end_date=args.end_date)
    md_report.write(md_report_path, args.title)
