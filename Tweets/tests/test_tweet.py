from django.test import TestCase
from Tweets.models import TCtweets
from TUsers.models import TUser

class TweetsTestCase(TestCase):
    def setUp(self):
        testUser=TUser(username="mark_cuban")
        TCtweets.user.add(testUser)
    def test_create_tweet(self):
        self.assertEqual("Hi there!",TCtweets.objects.get(pk=1))