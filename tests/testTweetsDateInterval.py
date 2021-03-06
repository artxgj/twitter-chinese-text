import unittest
import json
import datetime
from tweetybird import TweetsDateInterval


class TweetsDateIntervalTestCase(unittest.TestCase):
    def setUp(self):
        self.tweetsDateRange = TweetsDateInterval('2020-11-01', '2021-02-01')

    def test_tweet_within_date_range(self):
        with open("tweet_2020.js") as f1:
            tweet = json.load(f1)
            self.assertTrue(self.tweetsDateRange(tweet))

    def test_tweet_date_before_date_range(self):
        with open("tweet_2012.js") as f1:
            tweet = json.load(f1)
            self.assertFalse(self.tweetsDateRange(tweet))

    def test_tweet_date_after_date_range(self):
        with open("tweet_2021.js") as f1:
            tweet = json.load(f1)
            self.assertFalse(self.tweetsDateRange(tweet))

    def test_contains_directly(self):
        self.assertTrue(datetime.datetime.strptime("2020-12-25 -0800", "%Y-%m-%d %z") in self.tweetsDateRange)
        self.assertFalse(datetime.datetime.strptime("2019-02-07 -0800", "%Y-%m-%d %z") in self.tweetsDateRange)


if __name__ == '__main__':
    unittest.main()
