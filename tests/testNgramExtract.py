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

    def test_ngrams_1_extract(self):
        tweet_data = {
            "edit_info": {
                "initial": {
                    "editTweetIds": [
                        "1371339791564873734"
                    ],
                    "editableUntil": "2021-03-15T06:57:39.227Z",
                    "editsRemaining": "5",
                    "isEditEligible": True
                }
            },
            "retweeted": False,
            "source": "<a href=\"http://twitter.com/#!/download/ipad\" rel=\"nofollow\">Twitter for iPad</a>",
            "entities": {
                "hashtags": [],
                "symbols": [],
                "user_mentions": [
                    {
                        "name": "DW 中文- 德国之声",
                        "screen_name": "dw_chinese",
                        "indices": [
                            "3",
                            "14"
                        ],
                        "id_str": "143810986",
                        "id": "143810986"
                    }
                ],
                "urls": [
                    {
                        "url": "https://t.co/bBWfcMpLU4",
                        "expanded_url": "https://p.dw.com/p/3qd96",
                        "display_url": "p.dw.com/p/3qd96",
                        "indices": [
                            "81",
                            "104"
                        ]
                    }
                ]
            },
            "display_text_range": [
                "0",
                "104"
            ],
            "favorite_count": "0",
            "id_str": "1371339791564873734",
            "truncated": False,
            "retweet_count": "0",
            "id": "1371339791564873734",
            "possibly_sensitive": False,
            "created_at": "Mon Mar 15 05:57:39 +0000 2021",
            "favorited": False,
            "full_text": "RT @dw_chinese: 阿斯利康公司表示，其疫苗的施打与血栓风险增加无直接相关，但荷兰丶爱尔兰丶丹麦丶挪威等国基於对副作用的担忧，纷纷暂停推广此疫苗。\n\nhttps"
                         "://t.co/bBWfcMpLU4",
            "lang": "zh"
        }
        abtweet = AbbreviatedTweet(tweet_data)
        tweet_ngrams = HZTweetNgram(1)
        ngrams_of_tweet = tweet_ngrams.extract(abtweet)
        print(ngrams_of_tweet)


if __name__ == '__main__':
    unittest.main()
