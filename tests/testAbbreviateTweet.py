import unittest
from twitter_objects import AbbreviatedTweet


class AbbreviatedTweetTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tweet = {
            "retweeted": False,
            "source": "<a href=\"http://twitter.com/#!/download/ipad\" rel=\"nofollow\">Twitter for iPad</a>",
            "entities": {
                "hashtags": [
                    {
                        "text": "用听的",
                        "indices": [
                            "14",
                            "18"
                        ]
                    }
                ],
                "symbols": [],
                "user_mentions": [
                    {
                        "name": "联合早报 Lianhe Zaobao",
                        "screen_name": "zaobaosg",
                        "indices": [
                            "3",
                            "12"
                        ],
                        "id_str": "39941478",
                        "id": "39941478"
                    }
                ],
                "urls": [
                    {
                        "url": "https://t.co/WIMPURCmvK",
                        "expanded_url": "https://www.zaobao.com.sg/podcast/finance-talk/story20210224-1126499",
                        "display_url": "zaobao.com.sg/podcast/financ…",
                        "indices": [
                            "114",
                            "137"
                        ]
                    }
                ]
            },
            "display_text_range": [
                "0",
                "137"
            ],
            "favorite_count": "0",
            "id_str": "1365569522434859015",
            "truncated": False,
            "retweet_count": "0",
            "id": "1365569522434859015",
            "possibly_sensitive": False,
            "created_at": "Sat Feb 27 07:48:39 +0000 2021",
            "favorited": False,
            "full_text": "RT @zaobaosg: #用听的 美股游戏驿站（GameStop）股价暴涨暴跌，被视为散户与华尔街机构投资者之间的一场对弈。\n\n期权（Options）在GameStop战役中发挥了什么作用？这种投资产品如何操作，有什么风险？https://t.co/WIMPURCmvK",
            "lang": "zh"
        }

    def test_text_without_entities_has_rt(self):
        tweet = AbbreviatedTweet(self.tweet)
        expected = 'RT :  美股游戏驿站（GameStop）股价暴涨暴跌，被视为散户与华尔街机构投资者之间的一场对弈。\n\n期权（Options）在GameStop战役中发挥了什么作用？这种投资产品如何操作，有什么风险？'
        self.assertEqual(expected, tweet.text_without_entities(skip_rt=False))

    def test_text_without_entities_no_rt(self):
        tweet = AbbreviatedTweet(self.tweet)
        expected = ':  美股游戏驿站（GameStop）股价暴涨暴跌，被视为散户与华尔街机构投资者之间的一场对弈。\n\n期权（Options）在GameStop战役中发挥了什么作用？这种投资产品如何操作，有什么风险？'
        self.assertEqual(expected, tweet.text_without_entities())

    def test_crazy(self):
        tweet_data = {
            "retweeted": False,
            "source": "<a href=\"http://twitter.com/#!/download/ipad\" rel=\"nofollow\">Twitter for iPad</a>",
            "entities": {
                "user_mentions": [
                    {
                        "name": "edX",
                        "screen_name": "edXOnline",
                        "indices": [
                            "3",
                            "13"
                        ],
                        "id_str": "567360618",
                        "id": "567360618"
                    }
                ],
                "urls": [
                    {
                        "url": "https://t.co/wxBitT41R9",
                        "expanded_url": "http://ow.ly/W225J",
                        "display_url": "ow.ly/W225J",
                        "indices": [
                            "69",
                            "92"
                        ]
                    }
                ],
                "symbols": [],
                "media": [
                    {
                        "expanded_url": "https://twitter.com/edXOnline/status/681112831438241792/photo/1",
                        "source_status_id": "681112831438241792",
                        "indices": [
                            "109",
                            "132"
                        ],
                        "url": "https://t.co/HzidaAkBz5",
                        "media_url": "http://pbs.twimg.com/media/CXPMgthUEAEAkca.jpg",
                        "id_str": "681112831010279425",
                        "source_user_id": "567360618",
                        "id": "681112831010279425",
                        "media_url_https": "https://pbs.twimg.com/media/CXPMgthUEAEAkca.jpg",
                        "source_user_id_str": "567360618",
                        "sizes": {
                            "small": {
                                "w": "680",
                                "h": "340",
                                "resize": "fit"
                            },
                            "thumb": {
                                "w": "150",
                                "h": "150",
                                "resize": "crop"
                            },
                            "medium": {
                                "w": "1024",
                                "h": "512",
                                "resize": "fit"
                            },
                            "large": {
                                "w": "1024",
                                "h": "512",
                                "resize": "fit"
                            }
                        },
                        "type": "photo",
                        "source_status_id_str": "681112831438241792",
                        "display_url": "pic.twitter.com/HzidaAkBz5"
                    }
                ],
                "hashtags": [
                    {
                        "text": "metal",
                        "indices": [
                            "93",
                            "99"
                        ]
                    },
                    {
                        "text": "science",
                        "indices": [
                            "100",
                            "108"
                        ]
                    }
                ]
            },
            "display_text_range": [
                "0",
                "132"
            ],
            "favorite_count": "0",
            "id_str": "681297111346974720",
            "truncated": False,
            "retweet_count": "0",
            "id": "681297111346974720",
            "possibly_sensitive": False,
            "created_at": "Mon Dec 28 02:14:23 +0000 2015",
            "favorited": False,
            "full_text": "RT @edXOnline: Introduction to Steel is now self-paced – learn more: https://t.co/wxBitT41R9 #metal #science https://t.co/HzidaAkBz5",
            "lang": "en",
            "extended_entities": {
                "media": [
                    {
                        "expanded_url": "https://twitter.com/edXOnline/status/681112831438241792/photo/1",
                        "source_status_id": "681112831438241792",
                        "indices": [
                            "109",
                            "132"
                        ],
                        "url": "https://t.co/HzidaAkBz5",
                        "media_url": "http://pbs.twimg.com/media/CXPMgthUEAEAkca.jpg",
                        "id_str": "681112831010279425",
                        "source_user_id": "567360618",
                        "id": "681112831010279425",
                        "media_url_https": "https://pbs.twimg.com/media/CXPMgthUEAEAkca.jpg",
                        "source_user_id_str": "567360618",
                        "sizes": {
                            "small": {
                                "w": "680",
                                "h": "340",
                                "resize": "fit"
                            },
                            "thumb": {
                                "w": "150",
                                "h": "150",
                                "resize": "crop"
                            },
                            "medium": {
                                "w": "1024",
                                "h": "512",
                                "resize": "fit"
                            },
                            "large": {
                                "w": "1024",
                                "h": "512",
                                "resize": "fit"
                            }
                        },
                        "type": "photo",
                        "source_status_id_str": "681112831438241792",
                        "display_url": "pic.twitter.com/HzidaAkBz5"
                    }
                ]
            }
        }

        t = AbbreviatedTweet(tweet_data)


if __name__ == '__main__':
    unittest.main()
