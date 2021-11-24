import argparse
import pathlib
import urllib.parse
import simple_markdown as md

from hanzi_helpers import next_hanzi_tweet
from twitter_objects import AbbreviatedTweet
from typing import List


class TweetAttributesForMarkdown:
    def __init__(self, tweet: AbbreviatedTweet):
        self.tweet_date = tweet.created_at
        self.tweet_source = tweet.user_mentions[0].name
        self.tweet_full_text = tweet.full_text

    def __repr__(self):
        return f"{self.tweet_date.isoformat()} || {self.tweet_source} " \
               f"|| {self.tweet_full_text}"


def x_markdown_report_hztweets(tweet_md_attrs: List[TweetAttributesForMarkdown], title: str) -> str:
    gt_params = dict(hi='en', tab='TT', sl='zh-CN', tl='en', op='translate')
    mdtb_rows = []
    tweet_md_attrs.sort(key=lambda twa: twa.tweet_date)
    for tweet_attrs in tweet_md_attrs:
        gt_params['text'] = tweet_attrs.tweet_full_text.replace('\\n', '')
        link = f"https://translate.google.com/?{urllib.parse.urlencode(gt_params)}"
        row = md.table_row([str(tweet_attrs.tweet_date), tweet_attrs.tweet_source,
                            md.link(tweet_attrs.tweet_full_text, link)])
        mdtb_rows.append(row)

    tbl = '\n'.join(mdtb_rows)
    report = f"""## {title}    

| UTC Date | Tweet Source | Tweet (click or tap to see Google Translation) |
|:-----------------|:-------------|:------------------|  
{tbl}
"""
    return report


def generate_tweet_google_trans_markdown_reports(tweets_js_filepath: str, title: str, partition_size: int = 401):
    lines = 0
    markdown_table: List[TweetAttributesForMarkdown] = []
    report_num = 1

    for tweet in next_hanzi_tweet(tweets_js_filepath):
        markdown_table.append(TweetAttributesForMarkdown(tweet))
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
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate markdown files of Chinese=text tweets")
    parser.add_argument('-tweet-js-path', type=str, required=True, help='twitter\'s tweet.js filepath')
    args = parser.parse_args()
    generate_tweet_google_trans_markdown_reports(args.tweet_js_path, "Tweets Collection for Studying Chinese")
