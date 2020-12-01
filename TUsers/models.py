from django.db import models
from Tweets.views import get_cur_time

class TUser(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    country = models.CharField(max_length=100,null=True)
    modified_time = models.CharField(max_length=50,default=get_cur_time())
    following = models.ManyToManyField('self',related_name='followers',symmetrical=False,blank=True)
    blocked = models.BooleanField(default=False)