import unittest
from src.hanzi_helpers import HZTweetNgram
from src.twitter_objects import AbbreviatedTweet


class NgramExtractTestcase(unittest.TestCase):
    def setUp(self):
        self.tweet = {
                "retweeted": False,
                "source": "<a href=\"http://twitter.com/#!/download/ipad\" rel=\"nofollow\">Twitter for iPad</a>",
                "entities": {
                    "hashtags": [],
                    "symbols": [],
                    "user_mentions": [
                        {
                            "name": "华尔街日报中文网",
                            "screen_name": "ChineseWSJ",
                            "indices": [
                                "3",
                                "14"
                            ],
                            "id_str": "46574977",
                            "id": "46574977"
                        }
                    ],
                    "urls": [
                        {
                            "url": "https://t.co/kI2JTZmaVS",
                            "expanded_url": "https://on.wsj.com/3tlLki7",
                            "display_url": "on.wsj.com/3tlLki7",
                            "indices": [
                                "96",
                                "119"
                            ]
                        }
                    ]
                },
                "display_text_range": [
                    "0",
                    "119"
                ],
                "favorite_count": "0",
                "id_str": "1435498913885089800",
                "truncated": False,
                "retweet_count": "0",
                "id": "1435498913885089800",
                "possibly_sensitive": False,
                "created_at": "Wed Sep 08 07:03:06 +0000 2021",
                "favorited": False,
                "full_text": "RT @ChineseWSJ: 比特币周二让萨尔瓦多见识到了其著名的波动性，这个中美洲国家刚刚成为世界上首个采用这种资产作为法定货币的国家。比特币从美东时间周一下午5点的水平一度下跌17%。 https:// t.co / kI2JTZmaVS",
                "lang": "zh"
            }

    def test_ngrams_extract(self):
        abtweet = AbbreviatedTweet(self.tweet)
        tweet_ngrams = HZTweetNgram(2)
        ngrams_of_tweet = tweet_ngrams.extract(abtweet)
        self.assertFalse('午点' in ngrams_of_tweet)


if __name__ == '__main__':
    unittest.main()
