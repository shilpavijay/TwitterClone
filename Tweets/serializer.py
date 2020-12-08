from rest_framework import serializers
from Tweets.models import TCtweets
from django import forms

class TCtweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCtweets
        fields = '__all__'

class TCValidator(forms.Form) :
    username = forms.CharField()
    tweet_text = forms.CharField()           