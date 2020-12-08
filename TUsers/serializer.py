from rest_framework import serializers
from TUsers.models import TUser

class TUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TUser
        fields = '__all__'
           