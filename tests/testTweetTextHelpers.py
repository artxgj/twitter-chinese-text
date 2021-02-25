import unittest
from tweetybird import tweet_full_text, tweet_urls, tweet_hashtags_text, tweet_text_minus_entities


class TweetTextHelpersTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tweet = {
            "tweet": {
                "retweeted": False,
                "entities": {
                    "hashtags": [
                        {
                            "text": "汽车芯片",
                            "indices": [
                                "98",
                                "103"
                            ]
                        },
                        {
                            "text": "疫苗",
                            "indices": [
                                "108",
                                "111"
                            ]
                        }
                    ],
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
                            "url": "https://t.co/SmnV9BB7m3",
                            "expanded_url": "https://p.dw.com/p/3oiQS",
                            "display_url": "p.dw.com/p/3oiQS",
                            "indices": [
                                "116",
                                "139"
                            ]
                        }
                    ]
                },
                "display_text_range": [
                    "0",
                    "139"
                ],
                "favorite_count": "0",
                "id_str": "1356600919270453255",
                "truncated": False,
                "retweet_count": "0",
                "id": "1356600919270453255",
                "possibly_sensitive": False,
                "created_at": "Tue Feb 02 13:50:38 +0000 2021",
                "favorited": False,
                "full_text": "RT @dw_chinese: 德国“疫苗峰会”结论总结：人们需要做好长期接种的准备，政府对于到夏末为全民提供疫苗的承诺不变，无法促成（疫苗的交付）速度加快，哪怕用钱也无法做到。\n\n由此推理 ➡️#汽车芯片 换不来 #疫苗 。 \n\nhttps://t.co/SmnV9BB7m3",
                "lang": "zh"
            }
        }

    def test_hashtags_text(self):
        self.assertEqual(["汽车芯片", "疫苗"],
                         tweet_hashtags_text(self.tweet))

    def test_urls(self):
        self.assertEqual(["https://t.co/SmnV9BB7m3"], tweet_urls(self.tweet))

    def test_full_text(self):
        self.assertEqual("RT @dw_chinese: 德国“疫苗峰会”结论总结：人们需要做好长期接种的准备，政府对于到夏末为全民提供疫苗的承诺不变，无法促成（疫苗的交付）速度加快，哪怕用钱也无法做到。\n\n由此推理 ➡️#汽车芯片 换不来 #疫苗 。 \n\nhttps://t.co/SmnV9BB7m3",
                         tweet_full_text(self.tweet))

    def test_text_minus_entities(self):
        self.assertEqual("RT : 德国“疫苗峰会”结论总结：人们需要做好长期接种的准备，政府对于到夏末为全民提供疫苗的承诺不变，无法促成（疫苗的交付）速度加快，哪怕用钱也无法做到。\n\n由此推理 ➡️ 换不来  。 \n\n",
                         tweet_text_minus_entities(self.tweet))


if __name__ == '__main__':
    unittest.main()
