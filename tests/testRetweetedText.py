import unittest
import json
from tweetybird import is_retweeted_text


class RetweetedTextTestCase(unittest.TestCase):
    def test_is_retweeted(self):
        with open("tweet_2020.js") as f1:
            self.assertTrue(is_retweeted_text(json.load(f1)))

    def test_is_not_retweeted(self):
        with open("tweet_2021.js") as f1:
            self.assertFalse(is_retweeted_text(json.load(f1)))


if __name__ == '__main__':
    unittest.main()
