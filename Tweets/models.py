from django.db import models
from Tweets.views import get_cur_time
from TUsers.models import TUser

class TCtweets(models.Model):
    username = models.ForeignKey(TUser,on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=100,null=True)
    time = models.CharField(max_length=50,default=get_cur_time())
    retweet = models.ManyToManyField("self")
    like = models.IntegerField(null=True)
    comment = models.ManyToManyField("self")

    def __str__(self):
        return self.tweet_text
       