from rest_framework import serializers
from Tweets.models import TCtweets

class TCtweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCtweets
        fields = '__all__'