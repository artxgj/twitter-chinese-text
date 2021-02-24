from typing import Dict
import json
import pprint


def extract_hashtags(tweet_dict: Dict[str, Dict]):
    htags = tweet_dict["tweet"]["entities"]["hashtags"]
    return [htag["text"] for htag in htags]


if __name__ == "__main__":
    hashtags = set()
    with open("chinese_text_tweet.json") as fp:
        for tweet in json.load(fp):
            hashtags.update(extract_hashtags(tweet))

    pprint.pprint(hashtags)
