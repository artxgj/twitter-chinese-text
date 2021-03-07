import datetime
import json
import urllib.parse
import simple_markdown as md

from typing import List, Tuple, Generator
from tweetybird import tweet_text_minus_entities, tweet_date, tweet_user_mentions, TWITTER_DATE_FORMAT

Tweets = Generator[Tuple[str, str, str], None, None]


def tweets_trans_mdtable(tweets: Tweets, title: str) -> str:
    params = dict(hi='en', tab='TT', sl='zh-CN', tl='en', op='translate')
    mdtb_rows = []
    sorted_tweets = sorted(tweets, key=lambda tweet: tweet[0], reverse=True)
    for tweet_date, user_mention, tweet_text in sorted_tweets:
        params['text'] = tweet_text.replace('\\n', '')
        link = f"https://translate.google.com/?{urllib.parse.urlencode(params)}"
        row = md.table_row([tweet_date, user_mention, md.link(tweet_text, link)])
        mdtb_rows.append(row)

    tbl = '\n'.join(mdtb_rows)
    report = f"""## {title}    

| Date | Source | Tweet (click or tap to see English translation |
|:-----------------|:-------------|:------------------|  
{tbl}
"""
    return report


def from_hztweets_json_file(filepath: str) -> Tweets:
    with open(filepath, "r") as f_in:
        tweets = json.load(f_in)
        for tweet in tweets:
            tweet_text = tweet_text_minus_entities(tweet).strip(': ')
            dt_tweet = datetime.datetime.strptime(tweet_date(tweet), TWITTER_DATE_FORMAT).strftime("%Y-%m-%d")
            yield dt_tweet, tweet_user_mentions(tweet), tweet_text


if __name__ == '__main__':
    md_report = tweets_trans_mdtable(from_hztweets_json_file('chinese_text_tweet.json'),
                                     "Tweets Collection for Studying Chinese")

    with open("study/tweets-study-chinese.md", "w") as f_out:
        f_out.writelines(md_report)
