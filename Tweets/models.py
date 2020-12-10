from django.db import models
from TUsers.models import TUser
from datetime import datetime

get_cur_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

class TCtweets(models.Model):
    username = models.ForeignKey(TUser,on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=100,null=True)
    time = models.CharField(max_length=50,default=get_cur_time)
    retweet = models.ManyToManyField(TUser,related_name="retweeted_users")
    like = models.ManyToManyField(TUser,related_name="liked_users")
    reply = models.ManyToManyField("self")     
    comment = models.CharField(max_length=100,null=True)