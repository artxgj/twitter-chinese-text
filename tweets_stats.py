import argparse
import pathlib
from collections import Counter
from twitter_objects import from_tweet_js_file, next_tweet


def count_sources(tweet_js_path: str) -> Counter:
    ctr = Counter()

    for tweet in next_tweet(from_tweet_js_file(tweet_js_path)):
        if not tweet.user_mentions:
            ctr['🍍None🍍'] += 1
        else:
            ctr[tweet.user_mentions[0].name] += 1

    return ctr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name, description="Generate markdown files of Chinese=text tweets")
    parser.add_argument('-tweet-js-path', type=str, required=True, help='twitter\'s tweet.js filepath')
    args = parser.parse_args()
    sources = count_sources(args.tweet_js_path)
    print(sources)
