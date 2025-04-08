import unittest
from etl.data_model import TweetModel

class TestTweetModel(unittest.TestCase):
    def test_valid_tweet(self):
        tweet_data = {
            "id": 123,
            "author": "James",
            "post_date": "2025-01-01T12:00:00",
            "clean_text": "example tweet",
            "comment_num": 7,
            "retweet_num": 3,
            "like_num": 2,
            "tokens": ["example", "tweet"]
        }
        tweet = TweetModel(**tweet_data)
        self.assertEqual(tweet.id, 123)
    
    def test_invalid_date(self):
        tweet_data = {
            "id": 123,
            "post_date": "invalid_date",
            "cleaned_text": "example tweet",
            "comment_num": 7,
            "retweet_num": 3,
            "like_num": 2,
            "tokens": ["example", "tweet"]
        }
        with self.assertRaises(ValueError):
            TweetModel(**tweet_data)

if __name__ == '__main__':
    unittest.main()
