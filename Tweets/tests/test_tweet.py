from django.test import TestCase
from Tweets.models import TCtweets
from TUsers.models import TUser

class TweetsTestCase(TestCase):
    def setUp(self):
        user1 = TUser.objects.create(username="lori",password="sharktank",country="USA")
        TCtweets.objects.create(username=user1,tweet_text="Hi there!")
    def test_create_tweet(self):
        user1 = TUser.objects.get(username='lori')
        self.assertEqual("Hi there!",TCtweets.objects.get(username=user1).tweet_text)