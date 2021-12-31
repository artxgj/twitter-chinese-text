import datetime
import json
import urllib.parse
from src import simple_markdown as md

from dataclasses import dataclass
from typing import Generator, List, Tuple
from tweetybird import tweet_text_minus_entities, tweet_date, tweet_user_mentions, TWITTER_DATE_FORMAT


@dataclass
class TweetTranslationAttributes:
    tweet_date: str
    source: str
    tweet_text: str

    def __repr__(self):
        return f"{self.tweet_date} || {self.source} || {self.tweet_text}"


TweetAttributes = Generator[Tuple[str, str, str], None, None]


def x_markdown_report_hztweets(tweet_attrs_list: List[TweetTranslationAttributes], title: str) -> str:
    gt_params = dict(hi='en', tab='TT', sl='zh-CN', tl='en', op='translate')
    mdtb_rows = []
    tweet_attrs_list.sort(key=lambda twa: twa.tweet_date)
    for tweet_attrs in tweet_attrs_list:
        gt_params['text'] = tweet_attrs.tweet_text.replace('\\n', '')
        link = f"https://translate.google.com/?{urllib.parse.urlencode(gt_params)}"
        row = md.table_row([tweet_attrs.tweet_date, tweet_attrs.source, md.link(tweet_attrs.tweet_text, link)])
        mdtb_rows.append(row)

    tbl = '\n'.join(mdtb_rows)
    report = f"""## {title}    

| Date | Source | Tweet (click or tap to see English translation) |
|:-----------------|:-------------|:------------------|  
{tbl}
"""
    return report


def from_hztweets_json_file(filepath: str) -> Generator[TweetTranslationAttributes, None, None]:
    with open(filepath, "r") as f_in:
        tweets = json.load(f_in)
        print(f"number of tweets: {len(tweets)}")
        for tweet in tweets:
            tweet_text = tweet_text_minus_entities(tweet).strip(': ')
            dt_tweet = datetime.datetime.strptime(tweet_date(tweet), TWITTER_DATE_FORMAT).strftime("%Y-%m-%d")
            yield TweetTranslationAttributes(dt_tweet, tweet_user_mentions(tweet), tweet_text)


def generate_tweet_google_trans_markdown_reports(tweets_json_filepath: str, title: str, partition_size: int = 401):
    lines = 0
    markdown_table: List[TweetTranslationAttributes] = []
    report_num = 1

    for tweet_attr in from_hztweets_json_file(tweets_json_filepath):
        markdown_table.append(tweet_attr)
        lines += 1
        if lines == partition_size:
            with open(f"study/tweets-study-chinese-{report_num:03}.md", "w") as f_out:
                f_out.writelines(x_markdown_report_hztweets(markdown_table, title))

            lines = 0
            report_num += 1
            markdown_table.clear()

    if len(markdown_table) > 0:
        with open(f"study/tweets-study-chinese-{report_num:03}.md", "w") as f_out:
            f_out.writelines(x_markdown_report_hztweets(markdown_table, title))


if __name__ == '__main__':
    generate_tweet_google_trans_markdown_reports('chinese_text_tweet.json', "Tweets Collection for Studying Chinese")
