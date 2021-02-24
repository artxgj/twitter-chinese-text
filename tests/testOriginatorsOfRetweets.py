import unittest
import json
from tweetybird import OriginatorsOfRetweets


class TestTweetOriginatorsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tweet_originators = OriginatorsOfRetweets('screen_name', ('CompSciFact', 'AlgebraFact'))

    def test_tweet_belongs_to_originators(self):
        with open("tweet_2012.js") as f1:
            tweet = json.load(f1)
            self.assertTrue(self.tweet_originators(tweet))

    def test_tweet_does_not_belong_to_originators(self):
        with open("tweet_2020.js") as f1:
            tweet = json.load(f1)
            self.assertFalse(self.tweet_originators(tweet))

    def test_tweet_by_self(self):
        with open("tweet_2021.js") as f1:
            tweet = json.load(f1)
            self.assertFalse(self.tweet_originators(tweet))

    def test_originators_names(self):
        originators_names = OriginatorsOfRetweets("name", ("Computer Science", "Algebra Etc."))
        with open("tweet_2012.js") as f1:
            tweet = json.load(f1)
            self.assertTrue(originators_names(tweet))


if __name__ == '__main__':
    unittest.main()
